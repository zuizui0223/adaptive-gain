"""Mock-only audit checks for same-network optical comparison opportunity."""
from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path
script=Path(__file__).with_name("source_spectrometer_same_network_feasibility_gate.py")
spec=importlib.util.spec_from_file_location("stage69b_opportunity",script)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def fake_source():
    out=[]
    for i in range(73):
        out.append({
            "spectral_original_species_name":f"Genus{i} species{i}",
            "NHM_literal_species_name_match":"YES" if i<55 else "NO",
            "original_2024_true_petal_UV_300_399_percent":str(i/2),
            "original_2024_true_petal_visible_400_700_percent":str(60-i/4),
        })
    return out


class SameNetworkSourceGateTests(unittest.TestCase):
    def test_exact_original_source_73_55_guard(self):
        self.assertEqual(len(mod.actual_spectra_by_name(fake_source())),73)
        with self.assertRaisesRegex(ValueError,"73_55"):
            mod.actual_spectra_by_name(fake_source()[:-1])

    def test_original_spectrum_physical_units_not_normalized_or_guide_class(self):
        a=fake_source();a[0]["original_2024_true_petal_UV_300_399_percent"]="101"
        with self.assertRaisesRegex(ValueError,"PHYSICAL"):
            mod.actual_spectra_by_name(a)

    def test_duplicate_source_species_rejected(self):
        a=fake_source();a[1]["spectral_original_species_name"]=a[0]["spectral_original_species_name"]
        with self.assertRaisesRegex(ValueError,"DUPLICATE"):
            mod.actual_spectra_by_name(a)

    def test_no_automatic_guild_absence_or_native_site_from_names(self):
        self.assertEqual(mod.MIN_VISITS_EACH,3)
        self.assertEqual(mod.MIN_ORIGINAL_UV_DIFFERENCE_PERCENT,1)
        self.assertEqual(mod.MIN_SOURCE_STUDIES_FOR_FURTHER_EXPLORATION,3)
        self.assertNotEqual(mod.key("Genus1 species1"),mod.key("Genus2 species2"))


if __name__=="__main__":
    unittest.main()
