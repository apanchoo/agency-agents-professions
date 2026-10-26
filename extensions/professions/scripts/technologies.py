"""Named tools grounded in source text, with role routing and separate evidence."""
from functools import lru_cache
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
TOOLS = []
PROBES = {
 'Docker': ('docker',), 'Docker Compose': ('docker',), 'Docker Hub': ('docker',),
 'LXC/LXD': ('lxc', 'lxd'), 'AWS CodeDeploy': ('codedeploy',),
 'ELK stack': ('elk', 'elasticsearch', 'logstash', 'kibana'),
 'NAPALM': ('napalm', 'naplam'), 'YAML': ('yaml', 'yalm'), 'Cisco DevNet': ('devnet',),
 'Visual Studio Code': ('vscode', 'vs code', 'visual'), 'GNU Octave': ('octave',),
 'Microsoft Excel': ('excel',), 'Microsoft Access': ('access',), 'Tableau Software': ('tableau',),
 'Autodesk Revit': ('revit',), 'SolidWorks': ('solid',), 'Power BI': ('power',),
 'Power Query': ('power',), 'Power Pivot': ('power',),
 'SOLIDWORKS Sustainability': ('sustain',), 'ANSYS Granta EduPack': ('granta',),
 'REST APIs': ('rest',), 'R': (), 'C': (), 'OPC UA': ('opc',), 'Raspberry Pi': ('raspberry',),
}


def tool(name, area, use, pattern=None, priority=50):
    pattern = pattern or r"(?<![\w])" + re.escape(name) + r"(?![\w])"
    TOOLS.append({"name": name, "area": area, "use": use, "pattern": pattern,
                  "priority": priority, "regex": re.compile(pattern, re.I),
                  'probes': PROBES.get(name, (name.casefold(),))})


tool('Docker', 'containers', 'Build and tag reproducible images; configure networks, volumes and runtime health checks.', r'\bDocker(?:files?)?\b', 1)
tool('Docker Compose', 'containers', 'Describe multi-service stacks, dependencies, networks and persistent volumes in a versioned Compose file.', r'\bdocker[ -]compose\b', 2)
tool('Kubernetes', 'containers', 'Define workloads and services; verify rollout readiness, resource limits, scaling and rollback.', priority=3)
tool('Ansible', 'configuration', 'Use inventories, reusable roles and idempotent playbooks; review check-mode and diff results.', priority=4)
tool('Terraform', 'infrastructure', 'Review infrastructure plans, isolate state and confirm the proposed resource changes before applying.', priority=5)
tool('Pulumi', 'infrastructure', 'Version infrastructure programs and inspect previews, dependencies and state changes.', priority=6)
tool('GitLab', 'delivery', 'Version code and pipeline definitions; separate build, test, package and deployment stages.', priority=7)
tool('Jenkins', 'delivery', 'Define repeatable pipelines, managed credentials, test reports and promotion gates.', priority=8)
tool('Git', 'versioning', 'Use branches, reviewable commits and tags to trace changes to deployed artifacts.', r'(?-i:\b(?:Git|GIT)\b)', 9)
tool('Podman', 'containers', 'Build and run containers with appropriate privileges, networking and persistent storage.', priority=10)
tool('Docker Hub', 'containers', 'Publish and retrieve explicitly tagged images; verify image provenance and access permissions.', r'\bDocker\s*Hub\b', 11)
tool('LXC/LXD', 'containers', 'Configure system containers, resource isolation, networks and storage.', r'\blxc\b|\blxd\b', 12)
tool('AWS CodeDeploy', 'infrastructure', 'Prepare deployment bundles and lifecycle hooks; check deployment health and rollback behavior.', r'\b(?:AWS\s+)?CodeDeploy\b', 13)
tool('pytest', 'testing', 'Create repeatable Python test suites with fixtures and readable failure reports.', priority=14)
tool('JUnit', 'testing', 'Test Java behavior with isolated cases and publish test results in the delivery pipeline.', priority=15)
tool('doctest', 'testing', 'Validate executable examples against their expected results.', priority=16)
tool('SonarQube', 'delivery', 'Inspect code-analysis findings and use explicit quality gates without treating scans as a complete review.', priority=17)
tool('ELK stack', 'observability', 'Centralize structured logs, define useful queries and verify incident investigation paths.', r'\bELK\b|\bElasticsearch\b|\bLogstash\b|\bKibana\b', 18)
tool('Nexus', 'delivery', 'Publish versioned build artifacts and verify repository access and artifact retrieval.', r'\bNexus\b', 19)
tool('Python', 'programming', 'Write maintainable scripts with explicit dependencies, input validation and automated tests.', priority=20)
tool('PowerShell', 'scripting', 'Automate administration with structured objects, explicit error handling and controlled credentials.', priority=21)
tool('Bash', 'scripting', 'Automate command-line workflows with checked exit statuses, quoting and reproducible inputs.', priority=22)
tool('Linux', 'systems', 'Configure services, permissions, processes and logs; verify recovery and service startup.', priority=23)
tool('Windows', 'systems', 'Administer services, access rights and event logs; document configuration and recovery checks.', priority=24)
tool('OpenStack', 'virtualization', 'Provision virtual compute, network and storage resources with explicit quotas and access controls.', priority=25)
tool('VMware', 'virtualization', 'Configure virtual machines, virtual networks and storage; distinguish snapshots from verified backups.', priority=26)
tool('VirtualBox', 'virtualization', 'Build reproducible virtual-machine labs and test network modes, shared resources and clean recovery.', priority=27)
tool('Paramiko', 'network_automation', 'Automate SSH operations with host-key verification, timeouts and checked command results.', priority=28)
tool('Netmiko', 'network_automation', 'Automate network-device sessions with platform-aware commands and configuration verification.', priority=29)
tool('NAPALM', 'network_automation', 'Use network drivers and structured state comparisons to validate configuration changes.', r'\bNapa?lm\b|\bNaplam\b', 30)
tool('YAML', 'configuration', 'Validate configuration structure, quoting and schema before deployment.', r'\bYAML\b|\bYALM\b', 31)
tool('YANG', 'network_automation', 'Describe network configuration and operational data with explicit models and validation.', priority=32)
tool('Cisco DevNet', 'network_automation', 'Use documented network APIs and reproducible labs to validate automation workflows.', r'\bCisco\s+DevNet\b', 33)
tool('Wireshark', 'network', 'Capture authorized traffic and interpret packet fields, protocol flows and capture limitations.', priority=34)
tool('Cisco Packet Tracer', 'network', 'Model a network lab and verify addressing, routing and service connectivity.', r'\b(?:Cisco\s+)?Packet\s*Tracer\b', 35)
tool('JavaScript', 'web', 'Implement browser behavior with explicit state, accessible interactions and tests.', r'\bJava\s*Script\b', 36)
tool('HTML', 'web', 'Structure pages with semantic elements, accessible names and meaningful document order.', r'\bHTML(?:5)?\b', 37)
tool('CSS', 'web', 'Build responsive layouts that preserve content, contrast and text enlargement.', r'\bCSS(?:3)?\b', 38)
tool('SQL', 'database', 'Write parameterized queries, explicit schemas and checks for data integrity and query behavior.', priority=39)
tool('MySQL', 'database', 'Define schemas and indexes; verify queries, transactions and backup restoration.', priority=40)
tool('PostgreSQL', 'database', 'Design schemas, constraints and query plans; validate migrations and restoration.', priority=40)
tool('PHP', 'web', 'Validate requests, separate application concerns and test server-side behavior.', priority=41)
tool('Java', 'programming', 'Structure typed application code with controlled dependencies, exception handling and tests.', priority=42)
tool('C++', 'programming', 'Make ownership, lifetime and interface contracts explicit; test boundary conditions.', r'(?<!\w)C\+\+(?!\w)', 43)
tool('C', 'programming', 'Make memory bounds, data representation and hardware interfaces explicit.', r'\blangage\s+C\b(?!\+)', 44)
tool('Visual Studio Code', 'development', 'Share workspace, debugging and task configuration without embedding credentials.', r'\bVS\s*Code\b|\bVisual\s+Studio\s+Code\b', 45)
tool('virtualenv', 'development', 'Isolate Python dependencies and record reproducible environment setup.', priority=46)
tool('Sphinx', 'documentation', 'Build and verify versioned technical documentation, including broken links and executable examples.', priority=47)
tool('Javadoc', 'documentation', 'Generate API documentation from maintained contracts and verify links and examples.', priority=48)
tool('R', 'statistics', 'Prepare reproducible statistical analyses with explicit packages, seeds and validation assumptions.', r'(?:logiciels?|langage|programmation|sous)\s*(?:statistiques?\s*)?[(:]?\s*R\b|\b(?:SAS|pandas)\s*[–,/\-]\s*R\b', 49)
tool('RStudio', 'statistics', 'Organize reproducible R projects, scripts, environments and analysis reports.', priority=49)
tool('SAS', 'statistics', 'Prepare data transformations and statistical analyses with traceable code and diagnostics.', r'(?:logiciels?\s+statistiques?|programmation\s+statistique)[\s\S]{0,70}?\bSAS\b|\bSAS\s*[–,/\-]\s*R\b|\blangage\s+SAS\b', 49)
tool('MATLAB', 'simulation', 'Model numerical systems, document units and assumptions, and compare simulation results against checks.', priority=50)
tool('Simulink', 'simulation', 'Define system blocks, solver settings and test inputs; distinguish simulation from physical validation.', priority=50)
tool('Scilab', 'simulation', 'Implement numerical calculations and simulations with reproducible inputs and numerical checks.', priority=50)
tool('LabVIEW', 'measurement', 'Build acquisition and instrumentation workflows with explicit sampling, calibration and error handling.', priority=50)
tool('GNU Octave', 'simulation', 'Run reproducible numerical models and check algorithm and precision assumptions.', r'\b(?:GNU\s+)?Octave\b', 50)
tool('Xcas', 'simulation', 'Check symbolic and numerical calculations against the problem assumptions and units.', priority=50)
tool('GeoGebra', 'simulation', 'Build inspectable mathematical models and verify parameter-dependent results.', priority=50)
tool('Microsoft Excel', 'office', 'Build auditable workbooks with clear inputs, formulas, units and reconciliation checks.', r'\b(?:Microsoft\s+)?Excel\b', 51)
tool('Power BI', 'data', 'Prepare data models and dashboards with defined measures, refresh rules and reconciliation checks.', r'\bPower\s*BI\b', 51)
tool('Microsoft Access', 'database', 'Design relational tables, keys and queries; verify input validation and relationships.', r'\bMicrosoft\s+Access\b|\b(?:logiciel|SGBD)\s+Access\b', 51)
tool('Tableau Software', 'data', 'Build dashboards with defined measures, appropriate encodings and traceable data sources.', r'\bTableau\s+(?:Software|Desktop|Prep|Public)\b|\blogiciel\s+(?-i:Tableau)\b', 51)
tool('Sage', 'business', 'Prepare traceable accounting workflows, reconciliations and controlled data exchanges.', r'\b(?:logiciel|progiciel|ERP)\s+Sage\b|\bSage\s+\d', 51)
tool('SAP', 'business', 'Map business processes, master data and controlled transactions in the configured ERP environment.', r'\b(?:ERP|progiciel|logiciel)\s+SAP\b|\bSAP\s+(?:ERP|S/4|HANA|Business)\b', 51)
tool('Autodesk Revit', 'cad', 'Coordinate BIM models, views and exchanged information; check geometry and model consistency.', r'\b(?:Autodesk\s+)?Revit\b', 52)
tool('AutoCAD', 'cad', 'Prepare drawings with controlled layers, units, dimensions and exchange settings.', priority=52)
tool('SolidWorks', 'cad', 'Build constrained models and assemblies; verify dimensions, tolerances and manufacturing outputs.', r'\bSolid\s*Works\b', 52)
tool('CATIA', 'cad', 'Prepare parametric models and assemblies with traceable design and manufacturing constraints.', priority=52)
tool('BIM', 'cad', 'Coordinate model information, naming, exchange requirements and discipline interfaces.', priority=53)
tool('QGIS', 'gis', 'Prepare coordinate systems, spatial data and reproducible geoprocessing checks.', priority=54)
tool('ArcGIS', 'gis', 'Define spatial data, coordinate systems and analysis workflows with documented assumptions.', priority=54)
tool('Arduino', 'embedded', 'Implement and test microcontroller I/O with verified electrical interfaces and timing.', priority=55)
tool('Raspberry Pi', 'embedded', 'Configure an embedded Linux environment and verify hardware interfaces and service startup.', priority=55)
tool('KiCad', 'electronics', 'Maintain schematic and PCB consistency; check electrical rules and manufacturing outputs.', priority=55)
tool('LTspice', 'electronics', 'Define circuit models and operating conditions; compare simulated behavior with acceptance criteria.', priority=55)
tool('Photoshop', 'design', 'Prepare editable image assets with controlled resolution, color space and export settings.', priority=56)
tool('Illustrator', 'design', 'Prepare scalable vector assets and verify geometry, type and export compatibility.', priority=56)
tool('InDesign', 'design', 'Build structured publication layouts with consistent styles, links and output checks.', priority=56)
tool('Blender', 'design', 'Prepare scene geometry, materials and render settings with reproducible output checks.', priority=56)
tool('Figma', 'design', 'Build reusable interface components and verify interaction, responsiveness and accessibility.', priority=56)
tool('Unity', 'design', 'Structure interactive scenes and verify target-platform behavior and performance.', priority=56)
tool('SPSS', 'statistics', 'Prepare statistical analyses with explicit variable definitions, transformations and diagnostic checks.', priority=57)
tool('LaTeX', 'documentation', 'Maintain structured technical documents and verify compilation, references and notation.', priority=57)
tool('Zotero', 'documentation', 'Maintain traceable reference metadata and verify citations against original sources.', priority=57)
tool('pandas', 'data', 'Prepare tabular transformations with explicit types, missing-value handling and reconciliation checks.', priority=40)
tool('Talend', 'data', 'Define ETL mappings, data-quality rules and repeatable import/export workflows.', priority=41)
tool('Power Query', 'office', 'Build reproducible data preparation steps and verify source refresh, types and row counts.', r'\bPower\s*Query\b', 42)
tool('Power Pivot', 'office', 'Define relationships and measures in a tabular model and reconcile aggregates with source data.', r'\bPower\s*Pivot\b', 43)
tool('MariaDB', 'database', 'Define relational schemas, constraints and queries; verify transactions and data restoration.', priority=44)
tool('Airtable', 'database', 'Model records and relationships in a low-code database with controlled access and export checks.', priority=45)
tool('Baserow', 'database', 'Structure collaborative data tables and verify relationships, permissions and data exports.', priority=45)
tool('NocoDB', 'database', 'Prepare a low-code database interface while preserving schema constraints and access controls.', priority=45)
tool('jQuery', 'web', 'Maintain browser interactions and DOM updates while checking events, accessibility and compatibility.', priority=46)
tool('WebGL', 'design', 'Prepare browser-rendered graphics and verify geometry, shaders, interaction and rendering performance.', priority=47)
tool('WebXR', 'design', 'Define immersive browser interactions and test device capability, input and user comfort constraints.', priority=47)
tool('Nagios', 'observability', 'Define host and service probes, thresholds and notification paths; test both healthy and failed checks.', priority=19)
tool('Centreon', 'observability', 'Configure monitored services, collection intervals and alert routing; verify incident visibility.', priority=19)
tool('NetFlow', 'observability', 'Inspect exported network-flow records, collection coverage and traffic baselines.', priority=35)
tool('SNMP', 'observability', 'Select monitored objects, secure credentials and polling intervals; verify retrieved values and units.', priority=35)
tool('IPv4', 'network', 'Plan addressing, subnets and routing; test required connectivity and filtering.', priority=58)
tool('IPv6', 'network', 'Plan addressing, neighbor discovery and routing; test reachability and security controls.', priority=58)
tool('DHCP', 'network', 'Define address pools, options and reservations; verify lease allocation and client behavior.', priority=58)
tool('DNS', 'network', 'Define records and resolution paths; verify authoritative answers, caching and failure behavior.', priority=58)
tool('VLAN', 'network', 'Define segmentation, tagging and allowed trunks; verify isolation and required inter-VLAN flows.', priority=58)
tool('VPN', 'network', 'Specify tunnel endpoints, routing and access controls; verify reachability and traffic protection.', priority=58)
tool('BGP', 'network', 'Define peerings and route policies; inspect advertised and received routes before and after changes.', priority=58)
tool('OSPF', 'network', 'Define areas, adjacencies and route costs; verify convergence and intended paths.', priority=58)
tool('REST APIs', 'interfaces', 'Specify resource contracts, authentication and error handling; test request and response behavior.', r'\bREST(?:ful)?\b', 59)
tool('JSON', 'configuration', 'Validate structured data and schemas; preserve types and check serialization round trips.', priority=59)
tool('XML', 'configuration', 'Validate document structure and schemas; control parsing and verify transformed output.', priority=59)
tool('MQTT', 'embedded', 'Define topics, broker access and delivery quality; test publishing, subscriptions and reconnects.', priority=60)
tool('LoRa', 'embedded', 'Specify radio parameters and deployment constraints; validate coverage and communication behavior.', priority=60)
tool('OPC UA', 'embedded', 'Define industrial information models, endpoint security and monitored values; verify interoperability.', priority=60)
tool('Modbus', 'embedded', 'Map registers, types and addressing; verify read/write behavior against the device contract.', priority=60)
tool('DIALux', 'simulation', 'Model lighting geometry and luminaire data; verify illuminance assumptions and calculation outputs.', priority=61)
tool('SOLIDWORKS Sustainability', 'environmental', 'Assess product life-cycle impacts with explicit material, process and transport assumptions.', r'\bSustain(?:ability|ibility)\s*\(\s*Solid\s*Works\s*\)', 52)
tool('ANSYS Granta EduPack', 'environmental', 'Compare material and process data and document environmental selection assumptions.', r'\b(?:ANSYS\s+)?Granta\s+Edu\s*Pack\b', 52)

AREA_LABELS = {'containers': 'Containers and orchestration', 'configuration': 'Configuration',
 'infrastructure': 'Infrastructure as code', 'delivery': 'Continuous delivery', 'versioning': 'Version control',
 'testing': 'Testing', 'observability': 'Observability', 'programming': 'Programming', 'scripting': 'Administration scripts',
 'systems': 'Operating systems', 'virtualization': 'Virtualization', 'network_automation': 'Network automation',
 'network': 'Network tools', 'web': 'Web technologies', 'database': 'Databases', 'development': 'Development environments',
 'documentation': 'Documentation', 'statistics': 'Statistical analysis', 'simulation': 'Numerical simulation',
 'measurement': 'Measurement and instrumentation', 'office': 'Spreadsheets', 'data': 'Data analysis', 'business': 'Business systems',
 'cad': 'Design and BIM', 'gis': 'Geographic information', 'embedded': 'Embedded systems', 'electronics': 'Electronic design',
 'design': 'Creative software', 'interfaces': 'Service interfaces', 'environmental': 'Environmental assessment'}


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text.lower()) if not unicodedata.combining(c))


def clean_text(text):
    # PDF line wrapping must not turn French "mes-sage" into the Sage product.
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    text = re.sub(r'https?://\S+', '', text)
    return text


def detect(text):
    text = clean_text(text)
    lower = text.casefold()
    found = [(entry, hit) for entry in TOOLS
      if (not entry['probes'] or any(probe in lower for probe in entry['probes']))
      and (hit := entry['regex'].search(text))]
    if not re.search(r'\bHTML5?\b|\bweb\b|\bJavaScript\b|feuilles?.{0,25}style', text, re.I):
        found = [(entry, hit) for entry, hit in found if entry['name'] != 'CSS']
    if any(entry['name'] == 'SOLIDWORKS Sustainability' for entry, _ in found):
        found = [(entry, hit) for entry, hit in found if entry['name'] != 'SolidWorks']
    return found


@lru_cache(maxsize=24)
def programme_source(programme_id):
    return json.loads((ROOT / f'sources/but-text/{programme_id}.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=24)
def programme_inventory(programme_id):
    source = programme_source(programme_id)
    programme, pages = source['programme'], source['pages']
    starts = sorted({module['page'] for module in programme['modules']})
    inventory = []
    for module in programme['modules']:
        next_page = next((p for p in starts if p > module['page']), len(pages) + 1)
        end = min(next_page, module['page'] + 4)
        found = {}
        for page in pages[module['page'] - 1:end - 1]:
            text = clean_text(page['text'].split('©Ministère')[0])
            for entry, hit in detect(text):
                if entry['name'] in found: continue
                found[entry['name']] = {'name': entry['name'], 'area': entry['area'], 'use': entry['use'], 'priority': entry['priority'],
                    'evidence': {'programme_id': programme_id, 'module_code': module['code'], 'module_title': module['title'],
                     'page': page['page'], 'matched_text': hit.group(), 'snippet': text[max(0, hit.start()-70):hit.end()+90].replace('\n', ' '),
                     'url': programme['url'] + '#page=' + str(page['page']), 'sha256': programme['sha256']}}
        inventory.extend((module, entry) for entry in found.values())
    return inventory


def extended_areas(title):
    text, areas = normalize(title), set()
    routes = [
      (r'devops|devsecops|cloud|administrat.*system|ingenieur.*system|architect.*infrastructure',
       'containers configuration infrastructure delivery versioning testing observability programming scripting systems virtualization network_automation development interfaces'),
      (r'reseau|telecom|cyber', 'network network_automation configuration scripting systems virtualization observability interfaces'),
      (r'developpe|programm|logiciel|web', 'programming web database versioning testing development interfaces'),
      (r'donnee|statisti|data|actuari|decisionnel', 'statistics data database office programming'),
      (r'comptab|gestion|financ|paie|controleur|commercial|logisti|qualite', 'office data business'),
      (r'dessinat|bim|cao|conception.*mecani|architect.*bat|emball|packaging|projeteur', 'cad'),
      (r'physi|thermi|energe|metrolog|mesur|materiau|mecani|electri|electron', 'simulation measurement'),
      (r'embarque|electron|automati|robot', 'embedded electronics'),
      (r'graphis|designer|infograph|multimedia|animation.*3d|animateur.*3d', 'design'),
      (r'geograph|geomati|topograph|cartograph', 'gis'),
      (r'environnement|ecoconcept|cycle.*vie|materiau|emball|packaging', 'environmental'),
    ]
    for pattern, group in routes:
        if re.search(pattern, text): areas.update(group.split())
    return areas


def select_technologies(fiche, matches):
    areas = extended_areas(fiche['rome']['intitule'])
    found = {}
    for match in matches:
        selected = {(module['code'], module['page']) for module in match['modules']}
        for module, entry in programme_inventory(match['programme_id']):
            direct = (module['code'], module['page']) in selected
            if not direct and entry['area'] not in areas: continue
            # General communication and personal-development resources are not a
            # technical endorsement. BIM is an explicit modelling example there.
            if re.search(r'anglais|expression|projet personnel|portfolio', normalize(module['title'])) and entry['area'] != 'cad': continue
            target = found.setdefault(entry['name'], {k: v for k, v in entry.items() if k != 'evidence'} | {'evidence': []})
            if entry['evidence'] not in target['evidence'] and len(target['evidence']) < 3:
                target['evidence'].append(entry['evidence'] | {'selection': 'selected_module' if direct else 'role_specific_toolbox'})
    return sorted(found.values(), key=lambda entry: (entry['priority'], entry['name']))


def validate_evidence(entries, matches):
    errors, names = [], set()
    allowed = {match['programme_id'] for match in matches}
    known = {entry['name'] for entry in TOOLS}
    for entry in entries:
        name = entry.get('name')
        if name not in known or name in names: errors.append(f'Invalid or duplicate technology: {name}')
        names.add(name)
        if not entry.get('evidence'): errors.append(f'Technology without evidence: {name}')
        for evidence in entry.get('evidence', []):
            try:
                assert evidence['programme_id'] in allowed, 'unrelated programme'
                source = programme_source(evidence['programme_id'])
                assert source['sha256'] == evidence['sha256'], 'source hash mismatch'
                modules = [m for m in source['programme']['modules'] if (m['code'], m['title']) == (evidence['module_code'], evidence['module_title'])]
                assert any(m['page'] <= evidence['page'] < m['page'] + 4 for m in modules), 'wrong module/page'
                assert 1 <= evidence['page'] <= len(source['pages']), 'page outside source'
                page = clean_text(source['pages'][evidence['page'] - 1]['text'])
                assert evidence['matched_text'] in page, 'quoted name missing from page'
                assert name in {tool['name'] for tool, _hit in detect(page)}, 'canonical tool not supported by the page'
            except (AssertionError, KeyError, IndexError) as error:
                errors.append(f'Invalid evidence for {name}: {error}')
    return errors


def summary(entries, link):
    if not entries: return ''
    names = ', '.join(entry['name'] for entry in entries[:16])
    return ('## Technologies and Software\n\n' + names + '.\n\n'
      'Select tools that fit the requested deliverable and the existing environment; these are options, not a mandatory stack. '
      f'Use the [technology toolbox]({link}) for their practical applications and verification points.\n')


def reference(entries):
    blocks = ['# Technology Toolbox', 'Select tools for the assignment, existing interfaces and available environment. '
      'Confirm installed versions and compatibility before implementation. A listed tool is an option, not a claim of access or a completed deployment.']
    for entry in entries:
        blocks.append(f"## {entry['name']}\n\n**{AREA_LABELS[entry['area']]}**. {entry['use']}")
    blocks.append('## Verification\n\nRetain the configuration or code, test inputs and observed results. '
      'Check the interfaces between selected tools and demonstrate the requested outcome. Report checks that have not been run.')
    return '\n\n'.join(blocks)
