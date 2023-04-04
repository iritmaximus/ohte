import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(10000)

    def test_created_with_correct_cash(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_created_with_empty_lunch_counts(self):
        self.assertEqual(self.kassapaate.edulliset + self.kassapaate.maukkaat, 0)

    def test_buy_edullinen_with_cash_exact_money(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_buy_edullinen_with_cash_exact_money_change(self):
        change = self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(change, 0)

    def test_buy_edullinen_with_cash_lunch_count(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_buy_edullinen_with_cash_insufficient_money(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_buy_edullinen_with_cash_insufficient_money_change(self):
        change = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(change, 200)

    def test_buy_edullinen_with_cash_insufficient_money_lunch_count(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)


class TestKassapaateAndMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_buuy_edullinen_with_card_charged(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 7.60 euroa")

    def test_buy_edullinen_with_card_success(self):
        return_bool = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(return_bool, True)

    def test_buy_edullinen_with_card_lunch_count(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_buy_edullinen_with_card_insufficient_card_money(self):
        maksukortti = Maksukortti(10)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(str(maksukortti), "Kortilla on rahaa 0.10 euroa")

    def test_buy_edullinen_with_cash_insufficient_money_failure(self):
        maksukortti = Maksukortti(10)
        return_bool = self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(return_bool, False)

    def test_buy_edullinen_with_card_insufficient_lunch_count(self):
        maksukortti = Maksukortti(10)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_buy_edullinen_with_card_insufficient_kassa_cash(self):
        maksukortti = Maksukortti(10)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_adding_funds_to_card_adds_to_kassa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_adding_funds_to_card_adds_to_card(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 11.00 euroa")
