import json, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class RepoTests(unittest.TestCase):
    def test_site_exists(self):
        self.assertTrue((ROOT/'site/index.html').is_file())
        self.assertTrue((ROOT/'site/search-index.json').is_file())
    def test_search_index_has_all_nav_pages(self):
        nav=json.loads((ROOT/'site-src/nav.json').read_text())
        idx=json.loads((ROOT/'site/search-index.json').read_text())
        self.assertEqual(sum(len(x[1]) for x in nav),len(idx))
    def test_env_validator_rejects_placeholder(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.env'; p.write_text('PLAINWIRE_ENV=production\nPLAINWIRE_PUBLIC_URL=https://x.test\nCOOKIE_SECURE=true\nPLAINWIRE_DB_HOST=db\nPLAINWIRE_DB_USER=plainwire\nPLAINWIRE_DB_PASS=CHANGE_ME\nPLAINWIRE_DB_NAME=plainwire\nPLAINWIRE_ENC_KEY=bad\n')
            r=subprocess.run(['python3',str(ROOT/'scripts/verify-production-env.py'),str(p)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertIn('ERROR:',r.stdout)

    def test_production_template_valid_after_secret_substitution(self):
        import base64, os
        src=(ROOT/'examples/production/plainwire.env.example').read_text()
        key=base64.b64encode(b'x'*32).decode()
        src=src.replace('CHANGE_ME_DB_PASSWORD','a'*64)
        src=src.replace('CHANGE_ME_REDIS_PASSWORD','b'*64)
        src=src.replace('CHANGE_ME_BASE64_32_BYTE_KEY',key)
        src=src.replace('CHANGE_ME_TURN_SECRET_AT_LEAST_32_BYTES','c'*64)
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'plainwire.env'; f.write_text(src)
            r=subprocess.run(['python3',str(ROOT/'scripts/verify-production-env.py'),str(f)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            self.assertIn('OK: no obvious production configuration problems found',r.stdout)

    def test_secret_generator_uses_plainwire_variable_names(self):
        r=subprocess.run([str(ROOT/'scripts/generate-secrets.sh')],capture_output=True,text=True,check=True)
        names={line.split('=',1)[0] for line in r.stdout.splitlines() if '=' in line}
        self.assertEqual(names,{
            'PLAINWIRE_ENC_KEY','PLAINWIRE_DB_PASS','PLAINWIRE_REDIS_PASSWORD',
            'PLAINWIRE_TURN_SECRET','PLAINWIRE_SCYLLA_PASSWORD'
        })

if __name__=='__main__': unittest.main()
