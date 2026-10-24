# mistraltemplate1 - guida per Claude (template Jekyll adattivo)

Template Jekyll per GitHub Pages: si clona, si cambia quasi solo `_config.yml` e il sito si adatta (lingua, URL, brand, menu, shop). Obiettivo e stato del lavoro: `PROGETTO_TEMPLATE.md`.

## Prima di toccare un clone (checklist)
1. `_config.yml`: `brand`, `description`, `default_lang`, `languages`, `whatsapp`, `contact_endpoint`, `ecommerce`. NON scrivere `url:`/`baseurl:` (li imposta GitHub Pages).
2. Menu: `_data/navigation.yml` (voci) + `_data/sottomenu.yml` (tendine, chiave = title identico). Url interni SENZA nome repo.
3. Home a blocchi: `_data/blocks_home.json` (campi id, nome, enabled, html). Modificare solo `html`, mai la struttura. Backup prima, rileggere il JSON dopo.
4. Colori/tema: `_data/tema.json`; kit blocchi in `assets/css/gaming.css` (nome storico, non rinominare; accento = `--gc-acc`).
5. Shop: `ecommerce: true` accende tutto. Dati in `_data/catalogo.json` (prezzi in centesimi) + una pagina per prodotto/categoria in `_negozio/` (esempi inclusi: `prodotto-esempio.md`, `categoria-esempio.md`).
6. Contenuti: `_pages/`, `_posts/`. Ogni pagina/articolo ha `ref:` (chiave di collegamento tra lingue).

## Regole d'oro
- ZERO valori fissi: niente nome repo, utente, dominio, telefono scritti nei layout/include/JS. Si usa `relative_url`, `site.*`, `_includes/site-name.html`.
- Admin (`admin/index.html`): `detectRepo()` ricava utente/repo dall'URL. Su dominio personalizzato chiede il repo una volta (localStorage `cms_repo`). Non hardcodarlo.
- `automation/publish.py`: percorso e URL ricavati da soli (cartella del file + remote git).
- Valore vuoto in config = funzione spenta, mai errore: i layout controllano che il campo sia pieno.
- Nessun plugin fuori da GitHub Pages. Build locale non disponibile su questo PC: si controlla online dopo il deploy.
- COMMENTARE i punti critici (layout, include, JS, CSS, config): dire cosa fa, cosa legge, cosa NON toccare.

## Multilingua (dettagli in `docs/MULTILINGUA.md`)
IT alla radice, altre lingue in `/xx/` create da admin > Lingue. Cambiare solo `default_lang` e `languages`. Traduzioni: `tr: copia|tradotto|da_aggiornare`, `tr_hash`; `automation/traduzioni_sync.py` + workflow marcano `da_aggiornare`. In Liquid niente `a contains b == false`: usare `{% if a contains b %}{% continue %}{% endif %}`.
**Lingue = cartelle (rilevamento automatico).** Clonare/rinominare una cartella `xx/` basta: `_includes/lingue-attive.html` la mette nel selettore (bandiera), `admin/js/lingue.js` (`lgDetect` + `lgNormalizza`, una volta per sessione aprendo admin > Lingue) la registra in `_config.yml` (languages + defaults), `_data/languages.yml`, `ui-text.yml` e corregge `lang`/`locale`/`permalink` dei file e gli url in `_data/i18n/xx/`; `traduzioni_sync.py` la vede da solo. La cartella e' la fonte di verita': il campo `lang:` dei file dopo un clone e' vecchio.
**Admin con lingua di lavoro** (`admin/js/lingua-admin.js`): selettore lingua nella barra in alto; Articoli, Pagine, Home e Menu usano gli STESSI editor ma leggono/scrivono `xx/_posts`, `xx/*.md`, `_data/i18n/xx/*`. Intercetta `window.fetch` e rimappa i path solo se lingua != base e sezione attiva in Articoli/Pagine/Menu; se il file lingua manca parte dalla copia della base (menu con url `/xx/`). Al salvataggio sistema il front matter (lang, locale, permalink, ref, `tr: tradotto` + `tr_hash`). NON riscrivere i path dentro index.html: aggiungere nuovi file da mappare in `mappa()`. `admin/js/core.js` e `articoli.js` NON sono caricati da index.html (legacy): la logica vera e' nello script inline di index.html.

## Eta' e date
MAI a mano: `<span data-eta="AAAA-MM-GG">N</span> anni`, `<span data-anni-da="AAAA">N</span> anni` (script in `_includes/footer/custom.html`).

## Design
MAI bordi laterali colorati su box, citazioni, avvisi, CTA. Box puliti con sfondo leggero o bordo uniforme.

## Pubblicare e lavorare
- Pubblicare con `..\pubblica.ps1` con `-Files` espliciti. Dopo il push NON aspettare la build: Mirco verifica da solo.
- Sessione interrotta: prima `read_file` e `git status --short`; spesso manca solo commit e push.
- PowerShell lungo: salvare in .ps1 e lanciare con `-NoProfile -ExecutionPolicy Bypass -File`. Mai chiamare funzioni RD/WR/CD/LS (alias: RD cancella!).
- Traduzioni: NIENTE GitHub Actions. L'hook `.githooks/pre-commit` lancia `automation/traduzioni_sync.py` a ogni commit (attivo con `git config core.hooksPath .githooks`, una volta per clone).
- Risposte brevissime, modifiche in una sola chiamata.

## Cose che funzionano
- Test senza build locale: simulare la logica JS dell'admin con node + `vm` (stub di `lgText`/`lgCommit` e albero finto) e lanciare `node --check` sul file. Esempio: `claudetemp\test_lingue.js` (clone en -> de rinominato).
- Rilevare le lingue dalle CARTELLE (non dal config) e normalizzare tutto il resto da li': evita config e cartelle fuori sync.
- Liquid senza plugin: costruire un array con `split` + `concat` + `uniq` dentro un include che fa solo `assign` (le variabili restano visibili a chi lo include).- Patch su file grandi con CRLF (admin/index.html): script node con `readFileSync`/`replace`/`writeFileSync` su stringhe esatte, mai edit multiriga a mano; poi `node --check` sui .js. Mock del wrapper fetch: `claudetemp\test_lingua_admin.js`.

SEO e lingue (24/10/2026)
- SEO per lingua: _includes/seo.html fa un solo meta robots (noindex se noindex:true o tr: copia), description per lingua da _data/languages.yml (chiave description; se manca NON la scrive), og:locale. hreflang in _includes/head/custom.html: solo versioni tradotte (stesso ref), x-default = lingua base. sitemap.xml propria (sostituisce jekyll-sitemap) con alternates hreflang, esclude noindex/copia/admin/404.
- Slug tradotti: lo slug e' il permalink del front matter; MAI scrivere a mano lo slug di un'altra lingua nei link: usare {% include url-ref.html ref="shop-negozio" %} (URL per ref nella lingua della pagina). Inglese: /en/shop/, /en/about-us/, /en/contact/, /en/category/, /en/shop/example-product/. carrello/ordine/grazie restano con slug italiano (noindex, e carrello.js controlla /grazie/). Una lingua clonata da admin parte con gli slug della base: tradurli cambiando permalink (e i link in menu/home).
- Lingua browser: script in head/custom.html. Solo prima visita, solo da pagine in lingua base, solo se esiste la versione tradotta; localStorage lang_pref = scelta ricordata (il click su bandiera/selettore la aggiorna); niente redirect per bot, ?nolang=1 o referrer dello stesso sito.


Elementi per pagina (24/10/2026)
- UN solo valore per tutte le liste: `per_page` in _config.yml (default 20), si cambia da admin > Impostazioni (10, 20, 50, 100, 200, 500). L'admin lo copia in localStorage 'cms_per_page' (getPerPage in admin/index.html); NON reintrodurre limiti separati per elenco.
- Admin: elenchi Articoli, Pagine e Prodotti usano getPerPage(); le miniature/metadati si leggono a gruppi di 6 (metaQueue in wp-elenchi.js) per non finire il limite API con 200-500 voci.
- Sito: assets/js/paginazione.js impagina blog, negozio e pagina categoria (it e en) con gli attributi data-pg, data-pg-item, data-per sul contenitore; le voci restano tutte nell'HTML. Filtri che usano hidden (pillole negozio) chiamano PgLista.refresh. Se aggiungi un nuovo elenco lungo: stessi tre attributi, niente codice nuovo.


Lezioni dal clone "cybersecurity" (24/10/2026)
- Home, Chi siamo e Servizi sono a blocchi con testi SEGNAPOSTO neutri (IT in `_data/`, EN in `_data/i18n/en/`). Stile `ent-*` in `assets/css/gaming.css`; i colori seguono `_data/tema.json` (accent = `--gc-acc`, accent_dark = `--gc-ink`): NON mettere `<style>` con colori nei blocchi.
- I JSON dei blocchi si generano con uno script node (JSON.stringify + rilettura con JSON.parse), mai a mano; apostrofi e accenti nei blocchi come entita' HTML (&#39; &egrave;).
- Dopo aver scritto/tradotto a mano le pagine di una lingua: `python automation/allinea_hash.py en` (imposta `tr: tradotto` e `tr_hash`). Senza, l'hook le marca `da_aggiornare`.
- Ogni pagina/articolo ha `ref:` anche in italiano (serve al collegamento tra lingue e al selettore).
- Dati, cifre e fonti nei testi: solo verificati sul web (cerca prima). Mai loghi clienti, recensioni, certificazioni o prezzi inventati.
- Il modulo contatti resta spento finche' `contact_endpoint` e' vuoto: chiederlo subito al cliente. Lo stesso per `whatsapp` ed `email`.
- Clone: `..\nuovo_sito.ps1` tiene `en/` di default (it,en). Con `-Lingue it` la cartella `en/` viene tolta: farlo solo se richiesto. `-Accento "#rrggbb"` imposta il colore.
- Pubblicare piu' file: `& ..\pubblica.ps1 -Repo x -Msg "..." -Files 'a','b'` (ora accetta anche `-Files a,b` da `-File`).
