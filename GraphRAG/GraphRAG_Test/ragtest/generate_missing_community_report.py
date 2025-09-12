import os
import json
import pandas as pd
from datetime import datetime
from openai import OpenAI

BASE_DIR = os.path.join('ragtest','output')
API_KEY = os.environ.get('GRAPHRAG_API_KEY') or os.environ.get('OPENAI_API_KEY')
API_BASE = 'https://api.siliconflow.cn/v1'
MODEL = 'Qwen/Qwen3-8B'
TARGET_COMMUNITY_IDS = [19]  # numeric community IDs to backfill
MAX_TEXT_CHARS = 6000  # truncate long text

assert API_KEY, 'GRAPHRAG_API_KEY environment variable not set.'

# Load parquet tables
communities = pd.read_parquet(os.path.join(BASE_DIR,'communities.parquet'))
reports_path = os.path.join(BASE_DIR,'community_reports.parquet')
reports = pd.read_parquet(reports_path)
entities = pd.read_parquet(os.path.join(BASE_DIR,'entities.parquet'))
relationships = pd.read_parquet(os.path.join(BASE_DIR,'relationships.parquet'))
text_units = pd.read_parquet(os.path.join(BASE_DIR,'text_units.parquet'))

existing_numeric = set(reports['community'].tolist())
missing_numeric = [cid for cid in TARGET_COMMUNITY_IDS if cid not in existing_numeric]
if not missing_numeric:
    print('No target communities are missing. Nothing to do.')
    raise SystemExit

print('Communities to backfill:', missing_numeric)

client = OpenAI(api_key=API_KEY, base_url=API_BASE)

new_rows = []
for cid in missing_numeric:
    crow = communities[communities['community']==cid]
    if crow.empty:
        print(f'Community {cid} not found in communities table, skipping.')
        continue
    crow = crow.iloc[0]
    entity_ids = list(crow['entity_ids']) if hasattr(crow['entity_ids'],'__iter__') else []
    rel_ids = list(crow['relationship_ids']) if hasattr(crow['relationship_ids'],'__iter__') else []
    tu_ids = list(crow['text_unit_ids']) if hasattr(crow['text_unit_ids'],'__iter__') else []

    ents_df = entities[entities['id'].isin(entity_ids)].copy()
    rels_df = relationships[relationships['id'].isin(rel_ids)].copy()
    tus_df = text_units[text_units['id'].isin(tu_ids)].copy()

    # Build context strings
    ents_str = '\n'.join(f"- {r.get('title') or r.get('human_readable_id') or r['id']} ({r.get('type','')})" for _,r in ents_df.iterrows()) or 'None'
    rels_str = '\n'.join(f"- {r.get('source_title','')} -> {r.get('target_title','')}: {r.get('description','')}" for _,r in rels_df.iterrows()) or 'None'
    # Concatenate text safely
    text_concat = ''
    if 'text' in tus_df.columns and not tus_df.empty:
        text_concat = '\n'.join(tus_df['text'].astype(str).tolist())
    text_excerpt = (text_concat[:MAX_TEXT_CHARS] + ('...<truncated>' if len(text_concat) > MAX_TEXT_CHARS else '')) if text_concat else 'No associated text.'

    system_instructions = (
        'You are an analyst generating a concise community report. '
        'Provide: (1) Title, (2) 3-5 sentence summary, (3) Key findings bullet list.'
    )
    user_prompt = f"""Community ID: {cid}\nTitle: {crow['title']}\nLevel: {crow['level']} Parent: {crow['parent']} Size: {crow['size']}\n\nEntities:\n{ents_str}\n\nRelationships:\n{rels_str}\n\nText Excerpt:\n{text_excerpt}\n\nReturn JSON with keys: title, summary, findings (array of strings)."""

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"system","content":system_instructions},{"role":"user","content":user_prompt}],
            temperature=0,
            max_tokens=512,
        )
        content = completion.choices[0].message.content.strip()
    except Exception as e:
        print('LLM call failed for community', cid, e)
        continue

    # Attempt to parse JSON within content
    parsed = None
    if content.startswith('{'):
        try:
            parsed = json.loads(content)
        except Exception:
            pass
    if parsed is None:
        # Fallback: wrap textual content
        parsed = { 'title': crow['title'], 'summary': content, 'findings': [] }

    title = parsed.get('title') or crow['title']
    summary = parsed.get('summary') or ''
    # Normalize findings into list of dicts with 'summary'/'explanation' like existing rows expect
    raw_findings = parsed.get('findings') or []
    findings = []
    if isinstance(raw_findings, list):
        for f in raw_findings:
            if isinstance(f, dict):
                summary = f.get('summary') or f.get('title') or (str(f)[:60])
                explanation = f.get('explanation') or f.get('detail') or f.get('description') or summary
            else:
                summary = str(f)[:80]
                explanation = str(f)
            findings.append({'summary': summary, 'explanation': explanation})
    findings_text = findings  # store structured, consistent with existing parquet examples

    full_content = f"# {title}\n\n## Summary\n{summary}\n\n## Findings\n{findings_text}".strip()
    full_content_json = json.dumps({
        'title': title,
        'summary': summary,
        'findings': findings,
        'community': int(crow['community'])
    }, ensure_ascii=False)

    # Derive rank heuristic: size * 0.5 (arbitrary small weighting); rating_explanation left simple.
    try:
        size_val = float(crow['size']) if crow['size'] not in (None,'') else 0.0
    except Exception:
        size_val = 0.0
    rank = size_val * 0.5
    rating_explanation = 'Auto-generated backfill.'

    new_rows.append({
        'id': crow['id'],
        'human_readable_id': crow['human_readable_id'],
        'community': int(crow['community']),
        'level': crow['level'],
        'parent': crow['parent'],
        'children': crow['children'],
        'title': title,
        'summary': summary,
        'full_content': full_content,
        'rank': rank,
        'rating_explanation': rating_explanation,
    'findings': findings_text,
        'full_content_json': full_content_json,
        'period': crow['period'],
        'size': crow['size'],
    })

if not new_rows:
    print('No new reports generated.')
    raise SystemExit

new_df = pd.DataFrame(new_rows)
combined = pd.concat([reports, new_df], ignore_index=True)
# Ensure consistent dtypes (optional minimal cast)
combined.to_parquet(reports_path, index=False)
print('Added', len(new_rows), 'community report(s).')

"""Improvement utilities below (can be invoked manually)"""

def clean(text):
    return (text or '').replace('\n',' ')[:400]

def regenerate_with_rich_prompt(community_id:int, max_report_words:int=600):
    """Regenerate a community report using the richer original community prompt template.
    This will REPLACE the existing row for the given community id if present.
    """
    # Load current data
    communities = pd.read_parquet(os.path.join(BASE_DIR,'communities.parquet'))
    reports = pd.read_parquet(reports_path)
    entities = pd.read_parquet(os.path.join(BASE_DIR,'entities.parquet'))
    relationships = pd.read_parquet(os.path.join(BASE_DIR,'relationships.parquet'))
    text_units = pd.read_parquet(os.path.join(BASE_DIR,'text_units.parquet'))
    row = communities[communities['community']==community_id]
    if row.empty:
        print(f"Community {community_id} not found.")
        return
    row = row.iloc[0]
    ent_ids = list(row['entity_ids'])
    rel_ids = list(row['relationship_ids'])
    tu_ids = list(row['text_unit_ids'])
    ents_df = entities[entities['id'].isin(ent_ids)][['id','title','type','description']]
    rels_df = relationships[relationships['id'].isin(rel_ids)][['id','source','target','description']]
    tus_df = text_units[text_units['id'].isin(tu_ids)]
    # Build tabular text similar to pipeline
    ents_lines = ['Entities','id,title,type,description'] + [f"{r.id},{r.title},{r.type},{clean(r.description)}" for r in ents_df.itertuples()]
    rels_lines = ['','Relationships','id,source,target,description'] + [f"{r.id},{r.source},{r.target},{clean(r.description)}" for r in rels_df.itertuples()]
    input_text = '\n'.join(ents_lines + rels_lines)
    # Inject into a concise version of the graph prompt
    prompt_template = (
        "You are an AI assistant that writes structured community reports. Return a single JSON object with keys: "
        "title, summary, rating, rating_explanation, findings (array of objects with summary,explanation). Limit to {max_report_length} words.\n"
        "Ground claims with Data references using record ids from Entities (use entity id), Relationships (relationship id). Do not fabricate ids.\n"
        "Input Data:\n{input_text}\n"
    )
    user_prompt = prompt_template.format(max_report_length=max_report_words, input_text=input_text)
    system_msg = "You generate well-grounded community intelligence reports. Focus only on provided data."  
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"system","content":system_msg},{"role":"user","content":user_prompt}],
        temperature=0,
        max_tokens=700,
    )
    raw = completion.choices[0].message.content.strip()
    try:
        data = json.loads(raw)
    except Exception:
        data = {"title": row['title'], "summary": raw, "rating": 0, "rating_explanation": "Parse failed", "findings": []}
    # Normalize findings
    norm_findings=[]
    for f in data.get('findings',[]) or []:
        if isinstance(f, dict):
            norm_findings.append({'summary': f.get('summary','').strip()[:200], 'explanation': f.get('explanation','').strip()})
        else:
            norm_findings.append({'summary': str(f)[:80], 'explanation': str(f)})
    data['findings']=norm_findings
    # Replace row in reports
    reports = reports[reports['community']!=community_id]
    new_row = {
        'id': row['id'],
        'human_readable_id': row['human_readable_id'],
        'community': int(row['community']),
        'level': row['level'],
        'parent': row['parent'],
        'children': row['children'],
        'title': data.get('title') or row['title'],
        'summary': data.get('summary',''),
        'full_content': raw,
        'rank': row.get('size',0),
        'rating_explanation': data.get('rating_explanation',''),
        'findings': data.get('findings',[]),
        'full_content_json': json.dumps(data, ensure_ascii=False),
        'period': row['period'],
        'size': row['size'],
    }
    reports = pd.concat([reports, pd.DataFrame([new_row])], ignore_index=True)
    reports.to_parquet(reports_path, index=False)
    print(f"Regenerated community {community_id} report.")

if __name__ == '__main__':
    # Optional: call regeneration for community 19 when script executed directly with ENV var REGENERATE_19=1
    if os.environ.get('REGENERATE_19')=='1':
        regenerate_with_rich_prompt(19)
