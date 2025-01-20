import logging
import os
from copy import copy
from indic_transliteration.vidyut_helper import dev, slp

import regex
from click.utils import make_default_short_help
from sanskrit_data.collection_helper import OrderedSet
from tqdm import tqdm
from vidyut.kosha import Kosha, PratipadikaEntry
from vidyut.lipi import transliterate, Scheme
from vidyut.prakriya import Data, Vyakarana, Sanadi, Krt, Pratipadika, Vibhakti, Vacana, Linga, Pada, Taddhita, \
  DhatuPada, Lakara, Purusha, Prayoga, Gana, Dhatu

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)
logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")



v = Vyakarana()
data = Data("/home/vvasuki/gitland/ambuda-org/vidyut-latest/prakriya")
code_to_sutra = {(s.source, s.code): s.text for s in data.load_sutras()}
kosha = Kosha("/home/vvasuki/gitland/ambuda-org/vidyut-latest/kosha")


def lookup_and_derive(shabda):
  if isinstance(shabda, str):
    entries = kosha.get(slp(shabda))
  else:
    entries = [shabda]
  if len(entries) == 0:
    logging.error(f"Can't get entry for {shabda}.")
    return
  for entry in entries:
    prakriyas = v.derive(entry)
    show_prakriyaa(prakriyas)
  pass


def show_prakriyaa(prakriyas):
  for p in prakriyas:
    steps = []
    for step in p.history:
      source = dev(step.source).replace('आस्ह्तद्ह्ययि', 'अष्टाध्यायी')
      url = ""
      if source == "अष्टाध्यायी":
        sutra = dev(code_to_sutra.get((step.source, step.code), "(??)"))
        url = f"[A](https://ashtadhyayi.github.io/suutra/{step.code[:3]}/{step.code})"
      detail = f"{source} {step.code} → {dev(','.join(step.result))} {sutra} {url}"
      steps.append(detail)
    md_newline = '  \n'
    logging.info(f"## {dev(p.text)}\n{md_newline.join(steps)}\n")


def derive_and_print_tinanta():
  pada = Pada.Tinanta(
    dhatu=Dhatu.mula(aupadeshika="BU", gana=Gana.Bhvadi),
    prayoga=Prayoga.Kartari,
    lakara=Lakara.Lat,
    purusha=Purusha.Prathama,
    vacana=Vacana.Eka,
  )
  lookup_and_derive(pada)


def derive_and_print_subanta():
  pada = Pada.Subanta(
    pratipadika=Pratipadika.basic(slp("सुमनस्")),
    linga=Linga.Pum,
    vibhakti=Vibhakti.Prathama,
    vacana=Vacana.Eka,
  )
  lookup_and_derive(pada)


def derive_and_print_kRdanta():
  spastaya = Dhatu.nama(Pratipadika.basic(slp("स्पष्ट")), nama_sanadi=Sanadi.Ric)
  kRdanta = Pratipadika.krdanta(spastaya, krt=Krt.kta)
  lookup_and_derive(kRdanta)


if __name__ == '__main__':
  derive_and_print_subanta()
  pass
  