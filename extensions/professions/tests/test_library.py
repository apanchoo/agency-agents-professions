"""Tests de scénarios : routage métier, preuves et export réellement autonome."""
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_library import ROOT, load, match_programmes, read_rome
from library import export_profile, search, runtime_issues
from runtime_profiles import folder_name
from english import tr
from technologies import detect, clean_text


class LibraryScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = {r["code"]: r for r in load(ROOT / "catalog.json")}
        cls.mapping = {r["code"]: r for r in load(ROOT / "data/rome-but-mapping.json")}
        cls.tmp_root = (ROOT / "tmp/tests").resolve()
        cls.tmp_root.mkdir(parents=True, exist_ok=True)

    def test_search_by_accent_and_appellation(self):
        self.assertIn("M1805", [r["code"] for r in search("developpeur")])
        self.assertIn("M1805", [r["code"] for r in search("Analyste-programmeur")])
        self.assertIn("M1805", [r["code"] for r in search("m1805", but="info")])

    def test_software_role_uses_software_workflow(self):
        matches = self.mapping["M1805"]["matches"]
        self.assertEqual("info", matches[0]["programme_id"])
        selected = [m for m in matches[0]["modules"] if m["kind"] == "sae"]
        self.assertTrue(any("REAL" in m["code"] for m in selected))

    def test_devops_keeps_its_delivery_tools_and_workflow(self):
        row = self.catalog['M1827']
        expected = {'Docker', 'Docker Compose', 'Kubernetes', 'Ansible', 'Terraform', 'GitLab', 'Jenkins'}
        self.assertTrue(expected.issubset(set(row['technologies'])))
        self.assertEqual('rt', self.mapping['M1827']['matches'][0]['programme_id'])
        self.assertNotIn('geii', row['but'])
        self.assertNotIn('LabVIEW', row['technologies'])
        skill = ROOT / row['skill']
        self.assertIn('rollback', skill.read_text(encoding='utf-8'))
        toolbox = (skill.parent / 'references/technologies.md').read_text(encoding='utf-8')
        for name in expected: self.assertIn('## ' + name + '\n', toolbox)

    def test_product_detection_rejects_french_words_and_unrelated_acronyms(self):
        names = {entry['name'] for entry, _hit in detect("Un tableau de bord, une société SAS, les services SAP, un mes-\nsage et il s’git d’un exemple.")}
        self.assertFalse(names & {'Tableau Software', 'SAS', 'SAP', 'Sage', 'Git'})
        names = {entry['name'] for entry, _hit in detect('Docker, docker-compose, Kubernetes, Terraform et Ansible; logiciels statistiques SAS – R.')}
        self.assertTrue({'Docker', 'Docker Compose', 'Kubernetes', 'Terraform', 'Ansible', 'SAS', 'R'}.issubset(names))
        names = {entry['name'] for entry, _hit in detect('Les modulations radio utilisent CSS (LoRa).')}
        self.assertIn('LoRa', names); self.assertNotIn('CSS', names)
        names = {entry['name'] for entry, _hit in detect('Analyse du cycle de vie : Sustainibility (SolidWorks), ANSYS Granta Edupack.')}
        self.assertIn('SOLIDWORKS Sustainability', names); self.assertNotIn('SolidWorks', names)

    def test_named_tools_have_page_level_evidence_outside_runtime(self):
        for code in ['M1827', 'M1805', 'H1502']:
            proof = load(ROOT / f'audit/metiers/{code}/provenance.json')
            for technology in proof.get('technologies', []):
                self.assertTrue(technology['evidence'])
                for evidence in technology['evidence']:
                    source = load(ROOT / f"sources/but-text/{evidence['programme_id']}.json")
                    page = source['pages'][evidence['page'] - 1]
                    self.assertIn(evidence['matched_text'], clean_text(page['text']))
                    self.assertEqual(source['sha256'], evidence['sha256'])

    def test_industrial_quality_is_not_biological_by_default(self):
        self.assertEqual("qlio", self.mapping["H1502"]["matches"][0]["programme_id"])

    def test_social_assistance_uses_relevant_path(self):
        matches = self.mapping["K1201"]["matches"]
        self.assertEqual("cs", matches[0]["programme_id"])
        self.assertTrue(any(".AS." in m["code"] for m in matches[0]["modules"]))

    def test_no_forced_but_for_general_practitioner(self):
        self.assertEqual([], self.catalog["J1102"]["but"])
        self.assertTrue((ROOT / self.catalog["J1102"]["agent"]).is_file())
        self.assertTrue((ROOT / self.catalog["J1102"]["skill"]).is_file())

    def test_parent_code_alone_does_not_create_thematic_link(self):
        fiche = {"rome": {"code_rome": "M1899", "intitule": "Exemple sans thème biologique"},
                 "definition": "Administration de machines virtuelles", "competences": {}}
        programme = {"id": "gb", "title": "Génie biologique", "rome_mentions": {"M1801": [4]},
                     "modules": [{"kind": "ressource", "code": "R1.01", "title": "Machines virtuelles", "page": 5,
                                  "evidence": "Administration de machines virtuelles", "url": "https://example.invalid/#page=5"}],
                     "url": "https://example.invalid/", "sha256": "x"}
        matches = match_programmes(fiche, {"code_rome_parent": "M1801"}, [programme],
                                   {"gb": {"prefixes": ["A13"], "terms": "agricol"}}, {})
        self.assertEqual([], matches)

    def test_official_record_is_preserved(self):
        fiches, _, _ = read_rome()
        original = next(f for f in fiches if f["rome"]["code_rome"] == "M1805")
        copied = load(ROOT / "audit/metiers/M1805/fiche.json")
        self.assertEqual(original, copied)

    def test_selected_pages_contain_real_module_codes(self):
        # Contrôle sur le texte paginé, indépendant du catalogue des modules.
        for code in ["M1805", "H1502", "K1201", "N1103", "K1903"]:
            for match in self.mapping[code]["matches"]:
                pages = load(ROOT / f"sources/but-text/{match['programme_id']}.json")["pages"]
                for module in match["modules"]:
                    page_text = re.sub(r"\s+", "", pages[module["page"] - 1]["text"]).upper()
                    self.assertIn(module["code"].upper(), page_text)

    def test_export_contains_usable_references_and_links(self):
        with tempfile.TemporaryDirectory(dir=self.tmp_root) as tmp:
            Path(tmp).resolve().relative_to(self.tmp_root)
            target = export_profile("M1805", Path(tmp) / "developer")
            row = self.catalog["M1805"]
            skill = target / row["skill"]
            self.assertTrue((skill.parent / "references/expertise.md").is_file())
            self.assertTrue((skill.parent / "references/practice.md").is_file())
            self.assertFalse((skill.parent / "references/fiche.json").exists())
            self.assertTrue((target / "audit/metiers/M1805/fiche.json").is_file())
            profile = target / row["agent"]
            self.assertEqual([], runtime_issues([profile, *skill.parent.rglob("*.md")]))
            for link in re.findall(r"\]\(([^)]+)\)", profile.read_text(encoding="utf-8")):
                if "://" not in link:
                    self.assertTrue((profile.parent / link).resolve().is_file(), link)
            with self.assertRaises(FileExistsError):
                export_profile("M1805", target)

    def test_profession_names_are_used_in_directories(self):
        row = self.catalog["M1805"]
        expected = "software-developer-m1805"
        self.assertEqual(expected, Path(row["agent"]).parent.name)
        self.assertEqual(expected, Path(row["skill"]).parent.name)
        for row in self.catalog.values():
            name = folder_name(row["code"], row.get("original_title", row["title"]))
            self.assertLessEqual(len(name), 64)
            self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)+$")

    def test_operational_expertise_keeps_full_activity_coverage(self):
        row = self.catalog["M1805"]
        text = (ROOT / row["skill"]).parent.joinpath("references/expertise.md").read_text(encoding="utf-8")
        fiche = load(ROOT / "audit/metiers/M1805/fiche.json")
        for group in fiche["competences"]["savoir_faire"]["enjeux"]:
            for item in group["items"]:
                self.assertIn(tr(item["libelle"]), text)

    def test_operational_documents_preserve_enrichment_without_origin(self):
        row = self.catalog["M1805"]
        skill = ROOT / row["skill"]
        self.assertEqual([], runtime_issues([ROOT / row["agent"], *skill.parent.rglob("*.md")]))
        practice = (skill.parent / "references/practice.md").read_text(encoding="utf-8")
        for match in self.mapping["M1805"]["matches"]:
            for module in match["modules"]:
                self.assertIn(tr(module["title"]), practice)

    def test_export_rejects_path_as_code(self):
        with tempfile.TemporaryDirectory(dir=self.tmp_root) as tmp:
            Path(tmp).resolve().relative_to(self.tmp_root)
            with self.assertRaises(ValueError):
                export_profile("../outside", Path(tmp) / "rejected")
            self.assertFalse((Path(tmp) / "rejected").exists())


if __name__ == "__main__":
    unittest.main()
