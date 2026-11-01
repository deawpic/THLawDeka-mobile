import os

files = [
    'techdocs/system_spec_and_implementation_plan.md',
    'AGENTS.md',
    'THLawDeka/AGENTS.md',
    '.agents/skills/backend-development/SKILL.md',
    '.agents/skills/frontend-development/SKILL.md',
    '.agents/skills/qa-automation/SKILL.md',
    '.agents/skills/software-architecture/SKILL.md',
    '.agents/skills/product-management/SKILL.md'
]

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
        hits_artifact = c.count('ARTIFACT')
        hits_files = c.count('/api/v1/files')
        hits_output = c.count('output/')
        print(f'{f}: ARTIFACT={hits_artifact}, /api/v1/files={hits_files}, output/={hits_output}')
