"""InfoHawk — single-user local investigation workbench."""
import os
import streamlit as st
from autosave import make_report, export_json
from modules import domainrecon, emailintel, phonelookup, leaksearch
from modules.runners import availability, run_tool

st.set_page_config(page_title='InfoHawk · Zadwen', page_icon='🦅', layout='wide')
st.markdown('''<style>
.stApp {background: linear-gradient(140deg, #08111e, #102338);}
.block-container {max-width: 1200px; padding-top: 2rem;}
h1 {letter-spacing: -.04em;} div[data-testid="stMetric"] {background:#142e43;padding:18px;border-radius:14px;}
</style>''', unsafe_allow_html=True)
st.session_state.setdefault('reports', [])
with st.sidebar:
    st.title('🦅 InfoHawk')
    st.caption('INTELLIGENCE WORKBENCH · v4.0')
    st.markdown('**Crafted by Zadwen**')
    section = st.radio('Workspace', ['Domain & DNS', 'Email', 'Phone', 'Username', 'Reports'])
    st.divider()
    key = st.text_input('HIBP API key', type='password', help='Optional; you can also set HIBP_API_KEY.')
    tools = availability()
    for name, present in tools.items():
        st.caption(f'{"🟢" if present else "⚪"} {name}: {"available" if present else "not installed"}')
    st.caption('Run locally. Use for your own accounts, public research, or authorized investigations.')
    if st.button('Clear session reports'):
        st.session_state.reports = []
        st.rerun()

st.title(section)
st.caption('Public signals. Clear provenance. Exportable findings.')
a, b, c = st.columns(3)
a.metric('Session reports', len(st.session_state.reports))
b.metric('Optional tools ready', f'{sum(tools.values())} / 2')
c.metric('Storage', 'In memory')


def show_report(report):
    st.caption(f"{report['module']} · {report['target']} · {report['created_at']}")
    result = report['result']
    if 'output' in result:
        st.write('Status:', result['status'])
        st.code(result['output'] or '(No output)', language=None)
        st.caption(result['note'])
        if result.get('output_truncated'):
            st.warning('Output was truncated at 128 KiB.')
    else:
        st.json(result)
    st.download_button('Download JSON', export_json(report), file_name=f"infohawk-{report['id'][:8]}.json",
                       mime='application/json', key=report['id'])


if section == 'Reports':
    st.info('Reports remain in this browser session until cleared or disconnected. Download to keep a copy; downloads can contain personal data.')
    if st.session_state.reports:
        st.download_button('Download all reports', export_json(st.session_state.reports),
                           file_name='infohawk-reports.json', mime='application/json')
        for report in reversed(st.session_state.reports):
            with st.expander(f"{report['module']} · {report['target']}"):
                show_report(report)
    else:
        st.write('Run a lookup to create your first report.')
else:
    descriptions = {
        'Domain & DNS': 'Query A, AAAA, MX, NS, TXT and CAA records using your system DNS resolver.',
        'Email': 'Check email syntax and domain DNS, query HIBP breach metadata, or run optional Holehe.',
        'Phone': 'Inspect offline numbering-plan metadata. This does not locate a device or identify its owner.',
        'Username': 'Run optional Sherlock. Matches are research leads and require manual verification.'}
    st.write(descriptions[section])
    with st.form('lookup'):
        target = st.text_input('Target', placeholder={
            'Domain & DNS': 'example.com', 'Email': 'you@example.com',
            'Phone': '+968 …', 'Username': 'username'}[section])
        operation = st.selectbox('Check', ['Domain checks', 'HIBP breaches', 'Holehe']) if section == 'Email' else section
        region = st.text_input('Default country code', value='OM') if section == 'Phone' else 'OM'
        submitted = st.form_submit_button('Run lookup', type='primary')
    if submitted:
        try:
            if not target.strip():
                raise ValueError('Enter a target first.')
            with st.spinner('Running lookup…'):
                if section == 'Domain & DNS':
                    result = domainrecon.lookup(target)
                elif section == 'Phone':
                    result = phonelookup.analyze(target, region)
                elif section == 'Username':
                    result = run_tool('sherlock', target)
                elif operation == 'Domain checks':
                    result = emailintel.analyze(target)
                elif operation == 'HIBP breaches':
                    result = leaksearch.check_breaches(target, key or os.getenv('HIBP_API_KEY', ''))
                else:
                    result = run_tool('holehe', target)
            report = make_report(operation, target.strip(), result)
            st.session_state.reports.append(report)
            st.session_state.reports = st.session_state.reports[-50:]
        except ValueError as exc:
            st.error(str(exc))
    relevant = [r for r in st.session_state.reports if r['module'] in (
        ['Domain checks', 'HIBP breaches', 'Holehe'] if section == 'Email' else [section])]
    if relevant:
        st.divider()
        show_report(relevant[-1])
