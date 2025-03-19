import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_luodun_kortin_saldo_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_kortin_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(3000)

        self.assertEqual(self.maksukortti.saldo_euroina(), 40.0)

    def test_kortin_saldo_vahenee_oikein(self):
        self.maksukortti.ota_rahaa(500)

        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)

    def test_kortin_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(2000)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
    
    def test_luodun_kassapaatteen_rahamaara_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_luodun_kassapaatteen_myydyt_lounaat_oikein(self):
        self.assertEqual(self.kassapaate.edulliset + self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_osto_toimii_kateisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(300)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)
        self.assertEqual(vaihtoraha, 60)

    def test_syo_edullisesti_kateisella_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_edullisesti_kateisella(300)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kassapaate_toimii_oikein_kun_syo_edullisesti_kateismaksu_hylataan(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(vaihtoraha, 200)

    def test_syo_maukkaasti_osto_toimii_kateisella(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)
        self.assertEqual(vaihtoraha, 100)

    def test_syo_maukkaasti_kateisella_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kassapaate_toimii_oikein_kun_syo_maukkaasti_kateismaksu_hylataan(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(300)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(vaihtoraha, 300)

    def test_syo_edullisesti_kortilla_maksun_onnistuessa(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 7.6)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_edullisesti_kortilla_maksun_epaonnistuessa(self):
        maksukortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 2)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_maukkaasti_kortilla_maksun_onnistuessa(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 6.0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_kortilla_maksun_epaonnistuessa(self):
        maksukortti = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 2)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kortille_rahan_lataaminen_toimii_oikein(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 1000)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1010)
        self.assertEqual(maksukortti.saldo_euroina(), 20.0)
    
    def test_kortille_negatiivisen_summan_lataaminen_ei_muuta_saldoa(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, -1000)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(maksukortti.saldo_euroina(), 10.0)
    

