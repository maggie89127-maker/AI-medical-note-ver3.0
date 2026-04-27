import streamlit as st
import re
import html as html_lib

st.set_page_config(page_title="學習病歷產生器", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;500&display=swap');

/* === 藍調莫蘭迪 Blue Morandi === */
:root{
  --pri:#5A7FA8;       --pri-d:#3A5F88;    --pri-l:#8AAFD0;
  --bg:#EEF3F8;        --bg-card:#F6F9FC;  --bg-deep:#E2EAF4;
  --text:#1E2E40;      --text-sub:#4A6070;
  --border:#C0D0E0;    --shadow:rgba(58,95,136,.09);
  --red:#C0392B;       --red-glow:#C0392B;
  --blue-hi:#1565C0;   --blue-glow:#74B9FF;
}

/* App background */
.stApp{font-family:'Noto Sans TC',sans-serif;background:linear-gradient(150deg,#EEF3F8 0%,#DDE8F4 100%)!important}
[data-testid="stAppViewContainer"]{background:transparent!important}
[data-testid="stHeader"]{background:transparent!important}
h1,h2,h3,h4{font-family:'Noto Sans TC',sans-serif!important;font-weight:700!important;color:var(--text)!important;letter-spacing:.02em}

/* Sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#E2EAF4 0%,#D4E0EE 100%)!important;border-right:1.5px solid var(--border)}
[data-testid="stSidebar"] h3{color:var(--pri-d)!important;font-size:1rem!important}
[data-testid="stSidebar"] label{color:var(--text-sub)!important;font-size:.85rem!important}

/* Header banner */
.header-banner{background:linear-gradient(135deg,#3A5F88 0%,#5A7FA8 55%,#7A9FC8 100%);padding:2.2rem 2.5rem;border-radius:16px;margin-bottom:1.5rem;color:#fff;position:relative;overflow:hidden;box-shadow:0 4px 20px rgba(58,95,136,.20)}
.header-banner::before{content:'';position:absolute;top:-50%;left:-20%;width:140%;height:200%;background:radial-gradient(circle at 20% 30%,rgba(255,255,255,.18) 0%,transparent 50%),radial-gradient(circle at 80% 70%,rgba(255,255,255,.10) 0%,transparent 55%)}
.header-banner h1{margin:0;font-size:1.9rem;color:#fff!important;position:relative;z-index:1;font-weight:700;text-shadow:0 2px 8px rgba(30,46,64,.25)}
.header-banner p{margin:.5rem 0 0;opacity:.92;font-size:.95rem;position:relative;z-index:1}

/* Section labels */
.section-label,.section-label-green,.section-label-purple,.section-label-terra{background:var(--pri);color:#fff;display:inline-block;padding:.4rem 1.2rem;border-radius:20px;font-weight:600;font-size:.88rem;margin-bottom:.6rem;box-shadow:0 2px 8px rgba(90,127,168,.28);letter-spacing:.03em}
.section-label-green{background:#4A7A90}
.section-label-purple{background:#6A70A8}
.section-label-terra{background:#5A7FA8}

/* Note cards */
.note-card{background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--pri);border-radius:12px;padding:1.05rem 1.35rem;margin:0 0 .72rem 0;font-size:.86rem;line-height:1.82;white-space:pre-wrap;font-family:'JetBrains Mono','Noto Sans TC',monospace;color:var(--text);box-shadow:0 1px 5px var(--shadow);transition:all .22s}
.note-card:hover{box-shadow:0 4px 16px var(--shadow);border-left-color:var(--pri-d);transform:translateY(-1px)}
.note-card .red{color:#C0392B;font-weight:700}
.note-card .blue{color:#1565C0;font-weight:700}
.nc-title{font-family:'Noto Sans TC',sans-serif;font-weight:700;font-size:.94rem;color:var(--pri-d);margin-bottom:.5rem;border-bottom:1.5px solid #D0E0F0;padding-bottom:.4rem;letter-spacing:.02em}

/* Variant cards */
.variant-card{background:#EAF2F8;border:1px solid #B8D0E4;border-left:4px solid #4A7A90;border-radius:12px;padding:.88rem 1.3rem;margin:0 0 .65rem 0;font-size:.84rem;line-height:1.78;white-space:pre-wrap;font-family:'JetBrains Mono','Noto Sans TC',monospace;color:var(--text)}
.variant-card .red{color:#C0392B;font-weight:700}
.variant-card .blue{color:#1565C0;font-weight:700}
.variant-label{font-size:.73rem;font-weight:700;color:#3A6070;margin-bottom:.2rem;letter-spacing:.06em;text-transform:uppercase}

/* Chat */
.chat-container{background:#EBF2F8;border:1px solid var(--border);border-radius:14px;padding:1rem;margin:.5rem 0;max-height:380px;overflow-y:auto}
.chat-msg-user{background:linear-gradient(135deg,var(--pri),var(--pri-d));color:#fff;border-radius:16px 16px 4px 16px;padding:.68rem 1.05rem;margin:.5rem 0;max-width:85%;margin-left:auto;font-size:.85rem;text-align:right;box-shadow:0 3px 10px rgba(58,95,136,.22)}
.chat-msg-ai{background:#fff;color:var(--text);border:1px solid var(--border);border-radius:16px 16px 16px 4px;padding:.68rem 1.05rem;margin:.5rem 0;max-width:85%;font-size:.85rem;line-height:1.65;white-space:pre-wrap}

/* Buttons */
.stButton>button{background:linear-gradient(135deg,var(--pri) 0%,var(--pri-d) 100%)!important;color:#fff!important;border:none!important;border-radius:11px!important;padding:.65rem 1.85rem!important;font-weight:600!important;font-size:.95rem!important;letter-spacing:.03em!important;transition:all .25s cubic-bezier(.4,0,.2,1)!important;box-shadow:0 3px 10px rgba(58,95,136,.22)!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 7px 22px rgba(58,95,136,.32)!important;filter:brightness(1.07)!important}
.stButton>button:active{transform:translateY(0)!important}
.stDownloadButton>button{background:linear-gradient(135deg,#4A7A90 0%,#2E5868 100%)!important;color:#fff!important;border:none!important;border-radius:11px!important;font-weight:600!important;box-shadow:0 3px 10px rgba(46,88,104,.2)!important}
.stDownloadButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 7px 22px rgba(46,88,104,.30)!important}

/* Inputs */
div[data-testid="stTextArea"] textarea{font-family:'JetBrains Mono','Noto Sans TC',monospace!important;font-size:.85rem!important;border-radius:11px!important;border:1.5px solid var(--border)!important;line-height:1.7!important;background:var(--bg-card)!important;color:var(--text)!important;transition:all .2s!important}
div[data-testid="stTextArea"] textarea:focus{border-color:var(--pri)!important;box-shadow:0 0 0 3px rgba(90,127,168,.16)!important}
div[data-testid="stNumberInput"] input,div[data-testid="stTextInput"] input{border-radius:11px!important;border:1.5px solid var(--border)!important;background:var(--bg-card)!important;color:var(--text)!important}
div[data-testid="stSelectbox"] > div > div{border-radius:11px!important;border:1.5px solid var(--border)!important;background:var(--bg-card)!important}
div[data-testid="stRadio"] label{color:var(--text)!important;font-weight:500!important}
div[data-testid="stRadio"] > div{background:#E8F0F8;padding:.65rem 1rem;border-radius:11px;border:1px solid var(--border)}

/* Info boxes */
.tips-box{background:linear-gradient(135deg,#E4EFF8 0%,#D8E8F4 100%);border:1px solid #B8D0E4;border-radius:11px;padding:.88rem 1.1rem;font-size:.82rem;color:#3A5070;line-height:1.6}
.safety-warning{background:linear-gradient(135deg,#EAE8F4 0%,#E0DAF0 100%);border:1px solid #C4BCDC;border-left:4px solid #6A70A8;border-radius:11px;padding:.78rem 1.1rem;font-size:.8rem;color:#403058;line-height:1.55;margin-bottom:.7rem}
.footer-disclaimer{background:linear-gradient(180deg,#E2EAF4 0%,#D4E0EE 100%);border-top:1.5px solid var(--border);padding:1.1rem 2rem;margin-top:2rem;font-size:.76rem;color:var(--text-sub);line-height:1.6;text-align:center;border-radius:14px 14px 0 0}
.model-badge{background:linear-gradient(135deg,#E4EFF8 0%,#D8E8F4 100%);border:1px solid #B8D0E4;border-radius:9px;padding:.5rem .85rem;font-size:.76rem;color:#3A5888;margin-top:.4rem;line-height:1.5;font-family:'JetBrains Mono',monospace}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{gap:.4rem;background:#DDE8F4;padding:.42rem;border-radius:13px;border:1px solid var(--border)}
.stTabs [data-baseweb="tab"]{border-radius:10px!important;font-weight:600!important;font-size:.9rem!important;color:var(--text-sub)!important;background:transparent!important;padding:.52rem 1.25rem!important;transition:all .2s!important}
.stTabs [aria-selected="true"]{background:#fff!important;color:var(--pri-d)!important;box-shadow:0 2px 10px var(--shadow)!important}

/* Alerts */
div[data-testid="stAlert"]{border-radius:11px!important;border:none!important}
[data-testid="stSuccess"]{background:#DDF0E8!important;color:#1A6040!important}
[data-testid="stInfo"]{background:#DCE8F8!important;color:var(--pri-d)!important}
[data-testid="stWarning"]{background:#F0EAD8!important;color:#604010!important}
[data-testid="stError"]{background:#F4DADA!important;color:#8A1A1A!important}

/* Misc */
.stCaption,div[data-testid="stCaptionContainer"]{color:var(--text-sub)!important;font-size:.78rem!important}
.stSpinner > div{border-top-color:var(--pri)!important}
::-webkit-scrollbar{width:7px;height:7px}
::-webkit-scrollbar-track{background:var(--bg);border-radius:8px}
::-webkit-scrollbar-thumb{background:var(--pri-l);border-radius:8px}
::-webkit-scrollbar-thumb:hover{background:var(--pri)}
.empty-placeholder{border:2px dashed var(--border);border-radius:15px;padding:4rem 2rem;text-align:center;color:var(--text-sub);background:var(--bg-card)}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PROMPTS
# ══════════════════════════════════════════════════════════════

SYSTEM_PROMPT_BASE = r"""You are {role_description}.

CRITICAL LANGUAGE RULE:
The ENTIRE medical note content MUST be written in ENGLISH. Even if the user input is in Chinese, you MUST write all clinical content in English.
The ONLY Chinese allowed is the section headers themselves (e.g. "主訴 (Chief Complaint)").
This is non-negotiable.

Your task is to convert raw patient encounter information into a structured medical note.

If information is incomplete, infer and expand using reasonable general medical knowledge. Do NOT fabricate extreme or unlikely findings.

PATIENT DEMOGRAPHICS (CRITICAL):
{demographics_rule}

PRONOUN RULE: Use the correct pronoun (he/him/his or she/her) consistently throughout the entire note based on the patient's gender.

ADMISSION SOURCE (CRITICAL — changes the whole Present Illness structure):
{admission_source_rule}

CRITICAL: The user may provide MULTIPLE blocks of information, each marked with a header:
1. Main clinical data (ER note, OPD note, SP script) — may contain consultation reply sections (會診回覆 / Consult / Consultation) embedded inside
2. "--- 補充資料 ---" — supplemental data (extra hx, later inquiries)
3. "--- 血液檢驗 ---" — CBC / DC / coagulation results
4. "--- 生化檢驗 ---" — liver / renal / electrolytes / CRP / cardiac markers / ABG
5. "--- 其他檢驗 ---" — urinalysis / microbiology culture / EKG / imaging / pathology
6. "--- 過去出院診斷 ---" — past discharge / ER diagnoses (IMPORTANT: see rule below)

HOW TO INCORPORATE EACH BLOCK:
- Supplemental data: wrap content with [[...]] in Present Illness ONLY.
- Lab blocks (血液/生化/其他): integrate into Present Illness (ER course paragraph for ER, OPD course paragraph for OPD). When describing, group by category when clinically meaningful (e.g. "CBC revealed leukocytosis... Biochemistry showed elevated CRP and AKI... Urinalysis showed pyuria..."). Do NOT wrap with [[...]]. Reflect in PE/Impression if relevant.
- Past diagnoses block: see the dedicated rule in Past History section below. The original wording / bullet formatting MUST be preserved.

CONSULTATION REPLY HANDLING (CRITICAL — TWO-PART RULE):
The ER/OPD note may contain a consultation reply section (identified by keywords like "會診", "Consult", "Consultation reply", "Consulted by [Specialty]", or a named specialist's note).

PART A — FOR IMPRESSION (DIAGNOSTIC AUTHORITY):
If the consultation reply contains an impression / diagnosis / assessment statement, the consultant's impression is CLINICALLY AUTHORITATIVE and MUST be adopted as the PRIMARY impression of this admission note. Do NOT write your own inferred diagnosis as the primary one — use the consultant's impression verbatim (or minimally rephrased for grammar). If the consultant lists several differentials, keep the consultant's ranking. If multiple specialists were consulted with differing impressions, list the most recent / most authoritative one first.

PART B — FOR PLAN:
Extract ALL specific recommendations from the consultation reply (medications, doses, further workup, follow-up, disposition advice) and include them as Plan items. DO NOT prefix them with "Per [Specialty] consult:" or any similar attribution. Write them as plain plan bullets in the same style as the rest of the plan. The student should see a unified Plan, not a labelled list of who said what. Do NOT omit any consultation advice.

Example:
  Input ER note contains: "Nephro consult: Impression: AKI stage 2 on CKD, likely pre-renal etiology. Recommend IV hydration, hold NSAIDs, recheck BUN/Cr in 48h."
  → Impression should use: "Acute kidney injury stage 2 on CKD, likely pre-renal etiology" (consultant's impression)
  → Plan should list: " - IV hydration with normal saline", " - Hold NSAIDs", " - Recheck BUN/Cr in 48h"  (NOT "Per Nephrology consult: ...")

--------------------------------------------------
OUTPUT FORMAT

CRITICAL SECTION DELIMITER RULE:
Separate each section with EXACTLY this delimiter on its own line:
===SECTION===

Sections in order:
主訴 (Chief Complaint)
現在病症 (Present Illness)
過去病史 (Past History)
個人病史 (Personal History)
系統整理 (Review of System)
理學檢查 (Physical Examination)
臨床臆斷 (Impression)
處理計畫 (Plan)

Each section starts with its header on the first line, then content below.

--------------------------------------------------
主訴 (Chief Complaint)
One concise sentence: symptom + duration.

===SECTION===

現在病症 (Present Illness)
{pi_style}

===SECTION===

過去病史 (Past History)
{past_hx_rule}

===SECTION===

個人病史 (Personal History)
Allergy, Alcohol, Smoking, Betelnut. If missing, assume "denied".

===SECTION===

系統整理 (Review of System)

HIGHLIGHTING RULE (CRITICAL):
When you change a ROS item from its default value, you MUST do TWO things:
1. Wrap the changed value with **double asterisks** (for red highlighting).
2. Prepend the marker "⚠" (warning sign) immediately before the double asterisks, inside the parentheses.

The item name stays as plain text with NO asterisks or markers.

Examples:
- Default: fever:( no) → Changed: fever:( ⚠**yes**)
- Default: dizziness:( no) → Changed: dizziness:( ⚠**yes**)
- Default: visual acuity:( normal) → Changed: visual acuity:( ⚠**impaired**)
- Unchanged items stay exactly as template: cough:( no)

The pattern inside parentheses for changed items is: ( ⚠**value**)
DO NOT put any asterisks or markers before the item name. ONLY the value inside ( ) gets marked.

GENDER CHECK (CRITICAL):
{gender_ros_rule}

NUMBERED LIST format.

##Template:
1. General：
    weakness:( no), fatigue:( no), anorexia:( no), fever:( no), insomnia:( no)
2. Integument (skin, hair and nails)：
    changes in color:( no), pruritus:( no), rash:( no), hair loss:( no)
3. HEENT：
    a. Head - headache:( no), dizziness:( no), vertigo:( no)
    b. Eyes - visual acuity:( normal), color vision:( normal), corrective lenses:( no), photophobia:( no), diplopia:( no), pain:( no)
    c. Ears - pain:( no), discharge:( no), hearing loss:( no), tinnitus:( no)
    d. Nose - epistaxis:( no), discharge:( no), stuffiness:( no), sense of smell:( normal)
    e. Throat - status of teeth:( normal), gums:( normal), dentures:( no), taste:( normal), soreness:( no), hoarseness:( no), lump:( no)
4. Respiratory：cough:( no), sputum:( no), hemoptysis:( no), wheezing:( no), dyspnea:( no)
5. CV：edema:( no), chest distress:( no), chest pain:( no), palpitation:( no), intermittent claudication:( no), cold limbs:( no), cyanosis:( no)
6. GI：dysphagia:( no), nausea:( no), vomiting:( no), abdominal distress/pain:( no), change in bowel habit:( no), hematemesis:( no), melena:( no), bloody stool:( no)
7. GU：urinary frequency:( no), hesitancy:( no), urgency:( no), dribbling:( no), incontinence:( no), dysuria:( no), hematuria:( no), nocturia:( no), polyuria:( no)
8. Metabolic and endocrine：growth:( fair), development:( normal), weight change:( no), heat/cold intolerance:( no), nervousness:( no), sweating:( no), polydipsia:( no)
9. Hematotologic: anemia:( no), easy bruising or bleeding:( no), lymphadenopathy:( no), transfusions:( no)
10. Neuropsychiatry：dizziness:( no), syncope:( no), seizure:( no), speech disturbance:( no), loss of sensation:( no), paresthesia:( no), ataxia:( no), weakness or paralysis:( no), tremor:( no), anxiety:( no), depression:( no), irritability:( no)
11. Musculoskeletal：joint pain:( no), stiffness:( no), limitation of motion:( no), muscular weakness:( no), muscle wasting:( no)

===SECTION===

理學檢查 (Physical Examination)

HIGHLIGHTING RULE (CRITICAL):
ONLY mark findings that are CLINICALLY ABNORMAL and DIFFERENT from the default template.
Wrap ONLY the abnormal finding text with **double asterisks** so it renders in red.

Rules:
- If a finding is NORMAL or NOT SPECIFICALLY MENTIONED in the clinical data → keep the default template text exactly as-is, with NO asterisks.
- If a finding is ABNORMAL → change the text AND wrap the abnormal part with **.
  Example: Conjunctivae: **pale**
  Example: **tenderness over RUQ**; No rebounding pain
- Do NOT add ** to section headers (GENERAL APPEARANCE, CHEST, etc.).
- Do NOT add ** to lines that remain at their default normal value.
- ALWAYS output the complete template below — do NOT skip any section, even if normal.

NO blank lines between PE items. Compact output.

## Template (fill in ALL sections every time):
GENERAL APPEARANCE:
    chronic ill looking
CONSCIOUSNESS:
    Clear, E 4 V 5 M 6
VITAL SIGNS:
    T:XX.X P:XX R:XX BP:XXX/XX SpO2:XX%
HEENT:
    Sclerae: NOT icteric
    Conjunctivae: not arrow pale
    Oral cavity: Intact oral mucosa
NECK:
    Supple
    No jugular vein engorgement
CHEST:
    Breath pattern: smooth, Bilateral symmetric expansion
    No USE OF accessory muscles
    Breathing sound: bilateral clear AND symmetric breathing sound
    Wheezing: No wheezing
    Crackles: No basal crackles
HEART:
    Regular heart beat without audible murmur
    No audible S3; No audible S4
ABDOMEN:
    flat and soft, normoactive bowel sound
    No tenderness; No rebounding pain
    No muscle guarding
    No Murphy's sign
BACK:
    No knocking pain over bilateral flank area
EXTREMITIES:
    No joint deformity
    Freely movable
    No pitting edema
    Peripheral pulse: symmetric
NEUROLOGICAL:
    Motor power: full in all extremities (5/5)
    Sensation: intact
    Deep tendon reflex: normoactive
    Coordination: intact
    No focal neurological deficit
SKIN:
    No petechiae OR ecchymosis
    No abnormal skin rash
    Skin intact
    No wound

===SECTION===

臨床臆斷 (Impression)
{imp_style}

===SECTION===

處理計畫 (Plan)
{plan_style}

--------------------------------------------------
IMPORTANT RULES
1. Read like a real hospital admission note.
2. Internal consistency across all sections.
3. If info limited, expand using common disease presentations.
4. ALL body text in English. Section headers may have Chinese.
5. No explanations. Only the note.
6. No AI filler phrases. Write like a real clinician.
7. MANDATORY: ROS changed values use ⚠ prefix followed by **value** inside parentheses (e.g. fever:( ⚠**yes**)). The ⚠ serves as an alert marker for abnormal items. PE abnormal findings use **double asterisks** only (no ⚠). Normal/unchanged items have NO asterisks.
8. MANDATORY: ===SECTION=== between every two sections.
9. MANDATORY: [[double brackets]] around supplemental-data content in Present Illness only. Do NOT use [[...]] for examination results data.
10. MANDATORY: Plan section uses PLAIN TEXT. ALL bullet items start with " - " (space-dash-space). NO Markdown, NO numbered lists, NO "*", "•", or "- " at line start. No trailing spaces before line breaks. Each item on its own line at the same level (no nesting or indentation).
11. MANDATORY (Impression antibiotic formatting — NEW FORMAT): When antibiotics are used for an infectious diagnosis, the format is:
     - Primary infectious diagnosis, r/o differentials
       AntibioticName (YYYY/MM/DD-)
    The antibiotic line MUST be INDENTED with EXACTLY 3 SPACES (NOT " - ", NOT a bullet, just 3 spaces) on the line immediately AFTER its parent diagnosis. If multiple antibiotics, each on its own 3-space-indented line. Format the date range as "(YYYY/MM/DD-)" — hyphen after the date means ongoing, no end date. Do NOT include dose. If start date not provided, use admission date. Non-antibiotic diagnoses stay as single-line bullets.
12. MANDATORY: Use correct pronouns (he/she, him/her, his/her) throughout based on patient gender.
13. MANDATORY: Tense consistency — past tense for history and events, present tense for current status.
14. MANDATORY: Write like a real clinician in a Taiwan hospital. Avoid AI-sounding language. No phrases like "comprehensive evaluation", "multifaceted approach", "it is noteworthy that". Be direct and clinical.
15. MANDATORY (Consultation → Impression): If the ER/OPD note contains a consultation reply with its own impression/diagnosis, you MUST adopt that consultant's impression as the PRIMARY impression of this admission note (see CONSULTATION REPLY HANDLING rule above).
16. MANDATORY (Consultation → Plan): Consultation recommendations become plain Plan bullets. Do NOT use "Per [Specialty] consult:" attribution prefix. The Plan should read as unified management, not a list of who recommended what.
17. MANDATORY (Past discharge diagnoses — preserve original formatting): If "--- 過去出院診斷 ---" block is provided, preserve the user's ORIGINAL WORDING and bullet format verbatim in the Past History section. Do NOT rewrite, reformat, or paraphrase. Only translate Chinese disease names to English if the rest of the note is in English — but keep the original line structure / bullets / numbering exactly as provided. The same chronic conditions must ALSO be summarized into (a) the "underlying disease of:" clause of the Present Illness opening sentence, and (b) the <Underlying status> list inside Impression. Do NOT duplicate the full past-diagnosis text in those two places — only summarize chronic / still-active conditions there.
18. MANDATORY (Present Illness brevity rules):
    a. NEVER mention VAS (Visual Analog Scale) scores or any numeric pain score (e.g. "pain score 7/10", "NRS 8"). Pain severity should be expressed in clinical language only if meaningful (e.g. "severe", "progressive").
    b. NEVER mention routine analgesics (e.g. Panadol / acetaminophen, NSAIDs, tramadol, morphine) or antipyretics given solely for symptom relief in the ER or OPD. These are assumed. Only mention a medication if its CHOICE is clinically significant in its own right (e.g. antibiotics, thrombolytics, antiepileptics, antidotes, steroids as treatment).
    c. Physical Examination section: ALWAYS output the complete template with all sections. Mark ONLY abnormal findings with **double asterisks** for red highlighting. Normal items keep the default template text as-is with no asterisks. Do NOT skip any section even if normal."""

PI_FULL_ER = r"""Narrative paragraph style for INTERNAL MEDICINE admission note — ER ADMISSION.
Write like a real intern/resident in a Taiwan hospital. Use professional clinical English, NOT AI-generated language.

TENSE RULES: Use past tense for history and events. Use present tense for current status and findings.

STRUCTURE:

FIRST SENTENCE (CRITICAL):
"This is a [age]-year-old [male/female] with underlying disease of [summarized past history], who presented with [chief complaint + duration]..."
(The "underlying disease of ..." summary should draw from "--- 過去出院診斷 ---" block if provided. Summarize — don't duplicate its full wording.)

Then continue with narrative paragraphs:
- Onset, duration, characteristics (LQQOPERA — focused, no redundancy)
- Associated symptoms, pertinent negatives
- Pre-hospital course (clinic visits, prior treatment, symptom progression)

SUPPLEMENTAL DATA PLACEMENT:
If supplemental data is provided, integrate it naturally into the narrative:
- BEFORE ER course if it relates to symptom history
- AFTER symptom description if it adds clinical context
- Integrated into timeline where chronologically appropriate
Still MUST keep [[...]] marking for supplemental content.

EXAMINATION RESULTS:
Integrate the three categories (血液檢驗 / 生化檢驗 / 其他檢驗) into the ER course section. Group by category when helpful (e.g. "CBC revealed leukocytosis... Biochemistry showed elevated CRP and AKI... Urinalysis showed pyuria..."). Do NOT wrap with [[...]].

MANDATORY LINE BREAK RULES for Present Illness:
1. When the narrative transitions to ER/hospital arrival (e.g. "At the emergency department," / "On arrival," / "Upon arrival,"), insert exactly ONE BLANK LINE before it to start a new paragraph.
2. The final sentence starting with "Under the impression of..." MUST have exactly ONE BLANK LINE before it to start a new paragraph.

ER COURSE paragraph:
- Vital signs as compact line: T:XX.X P:XX R:XX SBP:XXX DBP:XX E:X V:X M:X SPO2:XX%
- Lab: ONLY clinically significant abnormals (do not list all normal values)
- Imaging: one-sentence key findings
- ER meds: name only, no dosages. EXCLUDE routine analgesics (e.g. Panadol, Tramadol, Morphine given for pain control) and antipyretics (e.g. Paracetamol, Ibuprofen given for fever) — these are assumed by the reader. Only mention if the drug choice itself is clinically significant (e.g. antibiotics, antiepileptics, thrombolytics, antidotes).
- NEVER mention VAS (Visual Analog Scale) pain scores or numeric pain scores (e.g. "pain score 7/10"). Pain severity should be described in clinical terms if needed (e.g. "severe", "moderate").

FINAL LINE: Under the impression of ..., admitted for further management.

STYLE: Write like a real clinician. No AI filler phrases. Concise and professional."""

PI_FULL_OPD = r"""Narrative paragraph style for INTERNAL MEDICINE admission note — OPD ADMISSION (直接門診收住院).
Write like a real intern/resident in a Taiwan hospital.

TENSE RULES: past tense for history and events, present tense for current status.

STRUCTURE (MANDATORY — do NOT write an ER course):

FIRST SENTENCE:
"This is a [age]-year-old [male/female] with underlying disease of [summarized past history], who presented to the outpatient clinic with [chief complaint + duration]..."
(Underlying diseases summary draws from "--- 過去出院診斷 ---" block if provided. Summarize only — do NOT duplicate the full past-diagnosis text here.)

Continue with narrative:
- Onset, duration, characteristics (LQQOPERA)
- Associated symptoms, pertinent negatives
- Prior course: symptom progression, prior clinic visits, self-medication if any

OPD COURSE paragraph (MANDATORY — replace what would be the ER paragraph; INSERT ONE BLANK LINE BEFORE):
Describe what happened AT THE OPD:
- Who saw the patient ("At the [specialty] OPD, the attending physician evaluated the patient...")
- What workup was ordered or already done — integrate 血液檢驗 / 生化檢驗 / 其他檢驗 results here in prose
- Results that prompted admission (clinical reasoning)
- Why admission was advised (e.g. need for IV therapy, abnormal imaging requiring observation, further invasive workup, clinical deterioration)

CRITICAL — DO NOT write "At triage". DO NOT list GCS (E:V:M) unless specifically documented. DO NOT fabricate ER vital signs or an ER course. If OPD vital signs are explicitly provided, you may include them as: "Vital signs at OPD: T:XX.X P:XX R:XX BP:XXX/XX SPO2:XX%."
NEVER mention VAS pain scores or numeric pain scores. NEVER mention routine analgesics (Panadol, NSAIDs for pain) or antipyretics given at OPD — these are assumed. Only mention medications if clinically significant.

SUPPLEMENTAL DATA: integrate naturally with [[double brackets]].
EXAMINATION RESULTS: integrate into OPD course paragraph (no brackets). Group by category when helpful.

FINAL LINE (MANDATORY, own paragraph, ONE BLANK LINE BEFORE):
"Under the impression of [primary diagnosis], he/she was admitted from the OPD for further management."

FOCUS ANCHORS for OPD admission: (a) chief complaint, (b) workup already done at OPD, (c) specific reason admission was recommended.

STYLE: Write like a real clinician. No AI filler phrases."""

PI_SHORT_ER = r"""You are writing the Present Illness section as an experienced SURGICAL resident in a Taiwan hospital — ER ADMISSION.
Write like a REAL surgical admission note (discharge summary style). NOT like AI-generated text.

WRITING STYLE RULES:
- Use natural, concise, professional clinical English
- Use past tense for history, present tense for current status
- Use correct pronouns (he/she) consistently
- NO AI filler phrases, NO over-explanation
- Lab: ONLY clinically significant abnormals (e.g. leukocytosis, elevated CRP, AKI)
- Imaging: ONE sentence of key findings
- Do NOT fabricate rare or unlikely findings
- NEVER mention VAS / numeric pain scores (e.g. "pain score 7/10")
- NEVER mention routine analgesics (Panadol, NSAIDs, opioids given for pain control) or antipyretics — these are assumed. Only mention drugs if the choice itself is clinically significant (e.g. antibiotics, antiepileptics)

STRUCTURE (MUST follow this EXACT format):

PARAGRAPH 1 — Opening + underlying diseases (THIS IS THE ONLY PLACE WHERE BULLET LIST IS ALLOWED):

This is a [age]-year-old [male/female] with underlying disease of:
 - [disease 1, with relevant detail]
 - [disease 2]
 - [operation history if any]

(Underlying list draws from "--- 過去出院診斷 ---" if provided, summarized for the opening. The full original past-diagnosis text stays in Past History section unchanged.)

PARAGRAPH 2 — Chief complaint + symptom narrative (CONTINUOUS PROSE, NO bullets):

The patient suffered from [chief complaint + duration]. Accompanied with [associated symptoms].
The patient denied [pertinent negatives: fever, chest pain, SOB, etc.].
[Pre-ER course: visited clinic/OPD/other hospital, treatment received, symptom progression]
He/She visited [clinic/hospital], where [treatment/advice/referral].

(INSERT ONE BLANK LINE HERE)

PARAGRAPH 3 — ER course (NEW paragraph after blank line):

At triage, his/her vital signs were:
T:XX.X P:XX R:XX SBP:XXX DBP:XX E:X V:X M:X SPO2:XX%.
Laboratory data revealed [ONLY clinically significant abnormals from 血液檢驗 / 生化檢驗 blocks, described in prose].
[Other studies: urinalysis, microbiology, EKG findings if provided in 其他檢驗 block]
Imaging studies showed [one-sentence key findings].
[ER interventions: drug names only, no doses]

(INSERT ONE BLANK LINE HERE)

FINAL LINE (MANDATORY, must be on its own paragraph):

Under the impression of [primary diagnosis], he/she was admitted for further management.

CRITICAL RULES:
- The underlying disease list in paragraph 1 is the ONLY place that uses " - " bullet format
- ALL other content must be continuous prose paragraphs
- Examination results from 血液/生化/其他檢驗 blocks go into the ER paragraph. Do NOT wrap with [[...]]
- Supplemental data from "--- 補充資料 ---" should be integrated into the symptom narrative. MUST wrap with [[...]]
- The note should look like it was written by a real surgical resident, not by AI"""

PI_SHORT_OPD = r"""You are writing the Present Illness section as an experienced SURGICAL resident in a Taiwan hospital — OPD ADMISSION.
Write like a REAL surgical admission note. Do NOT fabricate an ER course.

WRITING STYLE: same as ER version — concise, professional, no AI filler.

STRUCTURE (MUST follow):

PARAGRAPH 1 — Opening + underlying diseases (ONLY place bullet list is allowed):

This is a [age]-year-old [male/female] with underlying disease of:
 - [disease 1, with relevant detail]
 - [disease 2]
 - [operation history if any]

(Underlying list draws from "--- 過去出院診斷 ---" if provided, summarized. The full original past-diagnosis text stays in Past History section unchanged.)

PARAGRAPH 2 — Chief complaint + symptom narrative (CONTINUOUS PROSE):

The patient suffered from [chief complaint + duration]. Accompanied with [associated symptoms].
The patient denied [pertinent negatives].
[Prior course: symptom progression, prior clinic visits, self-medication if any]

(INSERT ONE BLANK LINE HERE)

PARAGRAPH 3 — OPD course (NEW paragraph):

At the [specialty] OPD, the patient was evaluated. [Describe physical findings briefly if notable.]
Workup revealed [clinically significant findings from 血液/生化/其他檢驗 blocks, in prose].
Imaging studies showed [one-sentence key findings, if any].
Given [reason for admission — e.g. need for IV therapy, surgical intervention, abnormal workup requiring inpatient management], admission was advised.

(INSERT ONE BLANK LINE HERE)

FINAL LINE (MANDATORY, own paragraph):

Under the impression of [primary diagnosis], he/she was admitted from the OPD for further management.

CRITICAL RULES:
- DO NOT write "At triage" or list GCS (E:V:M) unless explicitly provided
- DO NOT fabricate ER vital signs / ER interventions
- Focus anchors: chief complaint → OPD workup → reason for admission
- Underlying disease list is the only bullet area; rest is prose
- Examination results integrate into OPD course (no [[...]])
- Supplemental data uses [[...]]
- NEVER mention VAS / numeric pain scores
- NEVER mention routine analgesics or antipyretics given at OPD"""

IMP_FULL = """STRICT FORMAT RULE (ABSOLUTE — NO EXCEPTIONS):
Primary diagnosis items use " - " (space-dash-space) at line start.
ABSOLUTELY NO numbered lists (1. 2. 3.), NO "•", NO "*", NO "·".

CONSULTATION IMPRESSION PRIORITY:
If a consultation reply is present in the ER/OPD note and it contains an impression / diagnosis / assessment, USE THE CONSULTANT'S IMPRESSION as the primary diagnosis. Do NOT write your own inferred diagnosis when a consultant has already given one. Keep the consultant's differentials in their ranking order.

ANTIBIOTIC FORMATTING (CRITICAL — NEW FORMAT):
When antibiotics are used for an infectious diagnosis, the format is:
 - [Primary infectious diagnosis], r/o [differentials]
   [AntibioticName] (YYYY/MM/DD-)
   [AntibioticName2] (YYYY/MM/DD-)

The antibiotic line(s) MUST:
- Be on a SEPARATE line IMMEDIATELY AFTER the diagnosis line
- Start with EXACTLY 3 SPACES of indentation (NOT " - ", NOT a bullet, just 3 spaces)
- Contain antibiotic NAME + " (YYYY/MM/DD-)" where YYYY/MM/DD is the antibiotic start date
- NOT include dose, route, or frequency
- End with "-" inside the parentheses after the date, meaning ongoing (no end date yet)
- If start date is not provided, use the admission date

CORRECT example:
 - Community-acquired pneumonia, r/o aspiration pneumonia
   Ceftriaxone (2026/04/22-)
   Azithromycin (2026/04/22-)
 - Acute kidney injury on CKD stage 3 (eGFR 35)
 - Hyponatremia (Na 128)

Non-antibiotic related info (differentials) stays on the same line as the diagnosis, separated by commas or semicolons. Non-infectious diagnoses are single-line bullets with no indented sub-line.

WRONG (FORBIDDEN):
1. Community-acquired pneumonia
   - Antibiotics: Ceftriaxone
 - Pneumonia; Antibiotics: Ceftriaxone (D1: ...)   ← old format, no longer used

<Underlying status>
Use ONLY " - " (space-dash-space) for each item. NO blank lines between items. Compact list.
 - HTN, under medication control
 - DM type 2, on OHA
 - CKD stage 3

List chronic / still-active conditions here. Draw from "--- 過去出院診斷 ---" block if provided (summarize; the full original text stays in Past History unchanged). This stays within Impression — NOT a separate section. If the patient has renal impairment, note it here (e.g. CKD stage X, eGFR XX)."""

IMP_SHORT = """STRICT FORMAT RULE (ABSOLUTE — NO EXCEPTIONS):
All diagnosis items use " - " (space-dash-space) at line start. 2-4 items max.
NO numbered lists, NO "•", NO "*".

CONSULTATION IMPRESSION PRIORITY:
If a consultation reply provides an impression/diagnosis, adopt the consultant's impression as the primary diagnosis — do NOT override with your own inference.

ANTIBIOTIC FORMATTING (CRITICAL — NEW FORMAT):
When antibiotics are used, format as:
 - [Primary diagnosis with key differentials]
   [AntibioticName] (YYYY/MM/DD-)

The antibiotic line MUST start with EXACTLY 3 SPACES (not " - "), IMMEDIATELY after the diagnosis line. Multiple antibiotics → each on its own 3-space-indented line. NO dose. If start date not provided, use admission date.

Example:
 - Sepsis secondary to UTI
   Ceftriaxone (2026/04/22-)
 - AKI (eGFR 35)

<Underlying status>
Use ONLY " - " (space-dash-space). NO blank lines between items.
 - condition 1
 - condition 2
Draw from "--- 過去出院診斷 ---" if provided (summarize only). This stays within Impression."""

PLAN_FULL = """FORMAT RULE (ABSOLUTE — NO EXCEPTIONS):
Every bullet item MUST start with EXACTLY one space then a dash then a space: " - " (space-dash-space).
Do NOT start any line with "- " directly (no leading space = WRONG).
Do NOT use "•", "* ", "· ", numbers, nested lists, or any other format.
The sub-section headers (Diagnostic:, Therapeutic:, Measurable goal:) are plain text with NO bullet prefix.
No nested sub-items or indentation allowed. Each item is a single flat line.

CONSULTATION INTEGRATION (CRITICAL):
If the ER/OPD note contains a consultation reply (會診回覆 / Consult / Consultation), you MUST extract the consultant's SPECIFIC RECOMMENDATIONS (medications, further workup, follow-up, disposition, dose adjustments) and list them as ordinary Plan items under the appropriate sub-section.

DO NOT prefix these items with "Per [Specialty] consult:", "Per Nephrology consult:", "As recommended by ID:", or any similar attribution. The plan must read as a single unified management plan, not a labeled list of who said what. Integrate the recommendations seamlessly with any other Plan items.

Example transformation:
  Consultation reply says: "Nephro consult: Hold NSAIDs, IV hydration with NS, recheck BUN/Cr in 48h"
  → Plan should include:
       Therapeutic:
        - Hold NSAIDs
        - IV hydration with normal saline
       Diagnostic:
        - Recheck BUN/Cr in 48 hours
  (NOT "Per Nephrology consult: Hold NSAIDs...")

Output exactly like this:

Diagnostic:
 - Monitor renal function and electrolytes daily
 - Follow up blood culture results
 - Recheck BUN/Cr in 48 hours

Therapeutic:
 - Continue IV antibiotics
 - Fluid resuscitation with normal saline
 - Hold NSAIDs

Measurable goal:
 - Achieve afebrile status within 48 hours
 - Stabilize renal function within 5 days

Total 3-8 items. For drugs requiring renal dose adjustment, include adjustment recommendation."""

PLAN_SHORT = """FORMAT RULE (ABSOLUTE — NO EXCEPTIONS):
Every bullet item MUST start with EXACTLY " - " (space-dash-space). NO "- " at line start. NO "•", "* ", numbers, or nested lists.
Sub-section headers are plain text with NO bullet prefix.

CONSULTATION INTEGRATION (CRITICAL):
If consultation replies are present, extract specialist recommendations and write them as plain plan bullets. DO NOT use "Per [Specialty] consult:" or any attribution prefix — just write the recommendation as an ordinary plan item.

Diagnostic:
 - item
 - item

Therapeutic:
 - item
 - item

Measurable goal:
 - item (with timeframe)

Total 3-6 items. For drugs requiring renal dose adjustment, include adjustment."""

ADMISSION_ER_RULE = """The patient is admitted FROM THE EMERGENCY DEPARTMENT (急診入院).
Present Illness MUST include a proper ER course paragraph with:
- Triage / arrival phrase ("At triage, his/her vital signs were:" / "Upon arrival at the ER,")
- Compact vital signs line: T:XX.X P:XX R:XX SBP:XXX DBP:XX E:X V:X M:X SPO2:XX%
- Laboratory findings (clinically significant abnormals only, grouped by category if helpful)
- Imaging findings (one-sentence key findings)
- ER interventions / medications given
- Closing line: "Under the impression of ..., he/she was admitted for further management."
"""

ADMISSION_OPD_RULE = """The patient is admitted DIRECTLY FROM THE OUTPATIENT CLINIC (門診入院 / 直接門診收住院).
Present Illness MUST follow the OPD-admission structure. CRITICAL PROHIBITIONS:
- DO NOT write "At triage"
- DO NOT list ER vital signs or GCS (E:V:M) unless OPD vital signs are explicitly provided
- DO NOT fabricate an ER course that did not happen

Required structure (3 anchors):
1. Chief complaint + symptom narrative
2. OPD course paragraph: what studies were done at OPD, results that prompted admission
3. Specific reason admission was advised (e.g. need for IV therapy, abnormal workup requiring inpatient management, clinical deterioration)

Closing line: "Under the impression of [primary diagnosis], he/she was admitted from the OPD for further management."
"""

def build_system_prompt(surgical=False, age=None, gender=None, past_hx="", admission_source="ER"):
    # Demographics rule
    if age and gender:
        demographics_rule = (
            f"The patient is a {age}-year-old {gender}.\n"
            f"The FIRST sentence of Present Illness MUST start with: "
            f'"This is a {age}-year-old {gender} with underlying disease of [summarized past history], '
            f'who presented with [chief complaint]..."\n'
            f"Use {'he/him/his' if gender == 'male' else 'she/her'} pronouns throughout."
        )
    else:
        demographics_rule = (
            "Age and gender are NOT explicitly provided. Infer from clinical data if possible.\n"
            "The FIRST sentence of Present Illness should still follow the pattern: "
            '"This is a [age]-year-old [male/female] with underlying disease of ..., who presented with ..."'
        )

    # Gender-specific ROS rule
    if gender == "male":
        gender_ros_rule = (
            "The patient is MALE.\n"
            "Do NOT include female-specific items (e.g. menstruation, pregnancy, vaginal discharge)."
        )
    elif gender == "female":
        gender_ros_rule = (
            "The patient is FEMALE.\n"
            "Do NOT include male-specific items (e.g. prostate symptoms). "
            "Add gynecological items if clinically indicated."
        )
    else:
        gender_ros_rule = (
            "Determine the patient's sex from the clinical data.\n"
            "- For MALE patients: Do NOT include female-specific items.\n"
            "- For FEMALE patients: Do NOT include male-specific items."
        )

    # Past history rule — PRESERVE ORIGINAL FORMATTING if user provided past diagnoses
    if past_hx.strip():
        past_hx_rule = (
            "The user has provided past discharge / ER diagnoses in the '--- 過去出院診斷 ---' block.\n"
            "CRITICAL — PRESERVE ORIGINAL FORMATTING:\n"
            "You MUST reproduce the user's original wording and bullet format verbatim in this Past History section.\n"
            "- Do NOT rewrite, reformat, merge, or paraphrase.\n"
            "- Keep the exact line structure, bullet markers, numbering, and order as the user provided.\n"
            "- If the user wrote in Chinese, you MAY append a brief English translation in parentheses for disease names, but the original text MUST be kept.\n"
            "- If the user used numbered lists (1. 2. 3.), keep them numbered.\n"
            "- If the user used dashes or bullets, keep them exactly as-is.\n"
            "- Do NOT add your own items not present in the original.\n"
            "\n"
            "ADDITIONAL NOTE — the chronic / still-active conditions from this block MUST also appear in:\n"
            "(a) the 'underlying disease of:' clause of the Present Illness opening sentence, as a summary (not verbatim)\n"
            "(b) the <Underlying status> list inside Impression, as a summary (not verbatim)\n"
            "Only the Past History section keeps the ORIGINAL FULL TEXT."
        )
    else:
        past_hx_rule = (
            "No past discharge diagnoses were provided. List: Chronic diseases, Operation history, Previous admission history. "
            "Infer from main clinical data."
        )

    # Admission source rule + PI style selection
    if admission_source == "OPD":
        admission_source_rule = ADMISSION_OPD_RULE
        pi_style = PI_SHORT_OPD if surgical else PI_FULL_OPD
    else:  # ER
        admission_source_rule = ADMISSION_ER_RULE
        pi_style = PI_SHORT_ER if surgical else PI_FULL_ER

    role_desc = (
        "an experienced surgical resident and clinical teaching physician. "
        "You write admission notes in the style commonly used in Taiwan hospitals — "
        "concise, professional, discharge-summary-like. You avoid AI-sounding language "
        "and write like a real surgeon"
    ) if surgical else (
        "an experienced clinical physician and medical educator"
    )

    return SYSTEM_PROMPT_BASE.format(
        role_description=role_desc,
        pi_style=pi_style,
        imp_style=IMP_SHORT if surgical else IMP_FULL,
        plan_style=PLAN_SHORT if surgical else PLAN_FULL,
        demographics_rule=demographics_rule,
        gender_ros_rule=gender_ros_rule,
        past_hx_rule=past_hx_rule,
        admission_source_rule=admission_source_rule,
    )

LEARNING_ZONE_PROMPT = """You are a senior attending physician teaching a medical student.

Based on the following medical note, provide a clinical learning summary in Traditional Chinese (繁體中文). Use medical English terms where appropriate.

CRITICAL FORMATTING RULE: For ALL bullet-point lists, each item MUST be on its own line. Never put multiple items on the same line. Use "- " prefix for every item. This is essential for readability.

Use these exact markdown headers:

#### 📌 主要診斷與臨床推理
2-3 sentences on why this is the most likely diagnosis.

#### 🔍 鑑別診斷

Markdown table ranked by clinical likelihood:

| 排序 | 鑑別診斷 | 支持點 | 不支持點 |
|------|---------|--------|---------|
| 1 | Disease A | ... | ... |
| 2 | Disease B | ... | ... |

3-5 rows. One short sentence per cell.

#### 💊 治療原則與藥物建議
3-5 bullet points, each on its own line. Each: drug NAME, DOSE, ROUTE, FREQUENCY. Clinical rationale. Guideline reference.

RENAL DOSE ADJUSTMENT (CRITICAL): If the patient has ANY sign of renal impairment (elevated Cr, low eGFR, low CrCl, AKI, CKD), you MUST for EACH drug listed:
- State whether the drug requires renal dose adjustment (Yes/No)
- If Yes: state the patient's renal function (eGFR or CrCl value), then provide the EXACT adjusted dose with route and frequency.
  Example: "Colchicine: patient eGFR 29 → reduce to 0.3mg PO QD (standard: 0.6mg BID; per CrCl <30: halve dose and reduce frequency)"
  Example: "Teicoplanin: after loading doses, reduce maintenance to Q48H for CrCl <30"
- If No: state "no renal adjustment needed" briefly
- Always double-check the adjustment is correct per package insert or guideline

**⚠️ Guideline 符合度檢查**: Review if treatment aligns with guidelines. Flag discrepancies. Specifically check if renal-adjusted doses are correct.

#### 📖 Evidence-Based Guideline 參考
2-4 bullet points, each on its own line. Cite guideline name, organization, year.
Priority: IDSA, AHA, ACC, ESC, NCCN, ADA, GOLD, KDIGO, Surviving Sepsis Campaign.
If Taiwan differs: "台灣臨床實務差異：..."
If evidence limited: "Evidence is limited; practice may vary depending on institution."

#### 🔬 建議進一步檢查
3-5 bullet points, each on its own line, with clinical rationale.

#### ⚡ 學習重點摘要
3-5 high-yield pearls, each on its own line. Add a comparison table if useful.

#### 🔎 AI 自我查核

Part A — 病歷查核:
Review the medical note and check:
- Internal inconsistencies (e.g. ROS says no fever but PE shows T:39)
- Missing critical information
- Clinically implausible findings
- Impression vs Present Illness/PE consistency
- Plan vs Impression coverage
- If consultation replies were present in the source data, did the Impression adopt the consultant's diagnosis and did the Plan capture the consultant's recommendations (without "Per X consult:" prefix)?
- If past discharge diagnoses were provided, is the Past History section preserving the user's original wording / bullet format verbatim?

Part B — 學習重點查核:
Also review YOUR OWN learning content above and check:
- Are the differential diagnoses clinically reasonable for this presentation?
- Are the drug dosages correct per current guidelines?
- Are the cited guidelines accurate (correct organization, correct year, correct recommendation)?
- Are the suggested workup items appropriate and not excessive?
- Do the learning pearls contain any inaccurate or misleading statements?

Format as checklist, each item on its own line:
- ✅ or ⚠️ for each
- If all consistent: "✅ 本病歷及學習重點內容一致，未發現明顯矛盾或錯誤。"
- If issues found: list with ⚠️ and briefly explain

Rules:
- 繁體中文 for explanations, English for medical terms.
- Standard adult dosing from current guidelines.
- No AI filler. Write like a real attending.
- EVERY bullet point must be on its own line. No inline lists."""

CHAT_SYSTEM_PROMPT = """You are a senior attending physician answering questions about this patient case.
Answer based on the note. If not in note, say so and offer clinical reasoning.
Be concise. Use the student's language (繁體中文 or English). No AI filler.

===== MEDICAL NOTE =====
{note}
==========================="""

VARIANT_PROMPT = """You are an experienced clinical physician.

Rewrite this section as a SHORT/CONCISE version: keep only essential information, remove redundancy, aim for 40-60% of original length.

RULES:
- Output ONLY the rewritten content (no headers, no delimiters).
- English only. Clinically accurate.
- For Plan: each bullet MUST start with " - " (space-dash-space). NO "- " at line start. Sub-section headers (Diagnostic:, Therapeutic:, Measurable goal:) are plain text. No nested lists. If consultation recommendations are present in the full note, include them as ordinary plan bullets WITHOUT any "Per [Specialty] consult:" prefix.
- For Impression: diagnosis lines use " - " (space-dash-space). NO numbered lists (1. 2. 3.). If antibiotics are used, the antibiotic line(s) MUST be on separate lines IMMEDIATELY AFTER the diagnosis, INDENTED with EXACTLY 3 SPACES (not " - "), format: "   AntibioticName (YYYY/MM/DD-)". Do NOT merge antibiotics into the diagnosis line with semicolons. If a consultant's impression was used for the primary diagnosis, keep that diagnosis. <Underlying status> uses " - " bullets with no blank lines.
- For Present Illness (CRITICAL): The concise version MUST preserve the original paragraph/section structure. Do NOT collapse multiple paragraphs into one, and do NOT drop key structural sentences. Specifically:
    * Keep the OPENING sentence ("This is a [age]-year-old [male/female] with underlying disease of ..., who presented with ...")
    * Keep the SYMPTOM paragraph (onset, duration, associated symptoms, pertinent negatives) — shorten sentences but keep all key clinical facts
    * Keep the ER/OPD COURSE paragraph intact in structure — shorten lab/imaging descriptions to essential abnormals only
    * Keep the FINAL sentence ("Under the impression of ..., admitted for further management")
    * Preserve the ER/OPD distinction — never add ER content to an OPD note or vice versa
    * Keep [[double bracket]] markers around supplemental content
    * NEVER mention VAS / numeric pain scores. NEVER mention routine analgesics or antipyretics.
- For Past History: if the original preserves user-provided verbatim past-diagnosis text, do NOT reformat or paraphrase it in the concise version — keep it as-is.
- For ROS: numbered list, ⚠**value** pattern on changed items (⚠ before the **bold** value).
- For PE: no blank lines, **asterisks** on changed items.
- Write like a real clinician. No AI filler.

===== FULL NOTE (context) =====
{full_note}
====================================

SECTION: {section_title}
ORIGINAL:
{original_content}

Write the concise version:"""

# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def hl(text):
    """Highlight markers → colored spans. HTML-escaped first."""
    escaped = html_lib.escape(text)
    # ⚠**value** → red, displayed as (*value) for ROS abnormal items
    escaped = re.sub(r'⚠\*\*(.+?)\*\*', r'<span class="red">*\1</span>', escaped)
    # **value** → red (PE abnormal findings)
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<span class="red">\1</span>', escaped)
    # [[text]] → blue (supplemental data in PI)
    escaped = re.sub(r'\[\[(.+?)\]\]', r'<span class="blue">\1</span>', escaped)
    return escaped

def hl_plain(text):
    """Highlight markers → colored spans, then wrap each line in <div> to
    prevent Streamlit's Markdown engine from interpreting '- ' as list items
    or '<...>' as HTML tags. Produces compact, pure-text rendering.

    Impression antibiotic sub-lines (3-space indented, not " - ") are rendered
    with a visible hanging indent + deep-morandi-red weight so they appear
    visually nested under the parent diagnosis."""
    escaped = html_lib.escape(text)
    escaped = re.sub(r'⚠\*\*(.+?)\*\*', r'<span class="red">*\1</span>', escaped)
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<span class="red">\1</span>', escaped)
    escaped = re.sub(r'\[\[(.+?)\]\]', r'<span class="blue">\1</span>', escaped)
    lines = escaped.split('\n')
    parts = []
    for ln in lines:
        stripped = ln.strip()
        if stripped == '':
            # Preserve blank lines as a slim spacer (half-line height)
            parts.append('<div style="height:.45em"></div>')
        else:
            # Raw line (not stripped) — check for 3-space antibiotic indent
            if ln.startswith('   ') and not ln.startswith(' - '):
                parts.append(
                    '<div style="margin:0 0 0 1.8em;padding:0;line-height:1.75;'
                    'color:#FF6B6B;font-weight:700;text-shadow:0 0 8px rgba(255,80,80,.4)">' + stripped + '</div>'
                )
            else:
                parts.append(f'<div style="margin:0;padding:0;line-height:1.75">{ln}</div>')
    return ''.join(parts)

def anonymize(text):
    text = re.sub(r'[A-Z][12]\d{8}', 'X000000000', text)
    text = re.sub(r'09\d{2}[\-]?\d{3}[\-]?\d{3}', '09XX-XXX-XXX', text)
    text = re.sub(r'0\d[\-]?\d{4}[\-]?\d{4}', '0X-XXXX-XXXX', text)
    text = re.sub(r'(姓名|病患|患者|個案|名字)\s*[：:]\s*\S{2,5}', r'\1：XXX', text)
    text = re.sub(r'(病歷號|Chart No|chart no|病歷號碼)\s*[：:.]\s*\S+', r'\1：XXXXXXXX', text)
    return text

def parse_sections(raw):
    parts = re.split(r'\n*===SECTION===\n*', raw)
    out = []
    for p in parts:
        p = p.strip()
        if not p: continue
        lines = p.split('\n', 1)
        out.append((lines[0].strip(), lines[1].strip() if len(lines) > 1 else ""))
    return out

def detect_provider(ka, ko, kg):
    """Pick the first provider for which an API key was entered.
    Priority: Anthropic → OpenAI → Gemini."""
    if ka: return "Claude (Anthropic)", ka
    if ko: return "OpenAI", ko
    if kg: return "Gemini (Google)", kg
    return None, None

# ── Dynamic model resolution ─────────────────────────────────
# Rather than hard-coding model strings that go stale, we ask each provider's
# API for its available models and pick the newest / strongest one.
# The result is cached in st.session_state keyed by provider+key-fingerprint
# so we don't hit the /models endpoint every call.

def _key_fp(key):
    """Short non-sensitive fingerprint for cache key."""
    if not key: return ""
    return key[:4] + "…" + key[-4:] if len(key) > 10 else "key"

# ── Model-tier scoring helpers ─────────────────────────────────

def _claude_sort_key(mid):
    """Higher = better / newer for Claude models."""
    m = mid.lower()
    tier = 3 if "opus" in m else (2 if "sonnet" in m else (1 if "haiku" in m else 0))
    dm = re.search(r'(\d{8})$', mid)
    if dm:
        date = int(dm.group(1))
    else:
        vm = re.findall(r'\b(\d+(?:[-.]\d+)*)\b', mid)
        date = 0
        if vm:
            parts = [int(x) for x in re.split(r'[-.]', vm[-1]) if x.isdigit()]
            packed = 0
            for p in parts[:4]:
                packed = packed * 100 + p
            date = packed
    return (tier, date)

def _openai_score(mid):
    """Score for OpenAI text/chat models. Returns -1 to exclude."""
    m = mid.lower()
    if any(x in m for x in ["tts", "whisper", "dall", "embedding", "moderation",
                              "realtime", "audio", "transcribe", "image", "search",
                              "computer-use", "babbage", "davinci-00", "ada", "curie"]):
        return -1
    s = 0
    if re.match(r'^gpt-5', m):      s = 600
    elif re.match(r'^gpt-4\.5', m): s = 550
    elif re.match(r'^o4', m):       s = 530
    elif re.match(r'^o3', m):       s = 520
    elif re.match(r'^gpt-4o', m):   s = 500
    elif re.match(r'^o1', m):       s = 480
    elif re.match(r'^gpt-4-turbo', m): s = 450
    elif re.match(r'^gpt-4', m):    s = 400
    elif re.match(r'^gpt-3\.5', m): s = 200
    else: return -1
    if "mini" in m:    s -= 30
    if "nano" in m:    s -= 50
    if "preview" in m: s -= 10
    dm = re.search(r'(\d{4}-\d{2}-\d{2})$', m) or re.search(r'(\d{8})$', m)
    if dm:
        d = re.sub(r'\D', '', dm.group(1))
        s += min(int(d) // 10_000_000, 99)
    else:
        s += 5   # alias (no date) bonus
    return s

def _gemini_score(n):
    """Score for Gemini models. Returns -1 to exclude."""
    s = n.lower()
    if "embedding" in s or "aqa" in s: return -1
    base = 0
    vm = re.search(r'gemini-(\d+)\.?(\d+)?', s)
    if vm:
        base = int(vm.group(1)) * 100 + (int(vm.group(2) or 0))
    if "pro" in s:         base += 30
    elif "flash-lite" in s: base += 5
    elif "flash" in s:      base += 15
    if "exp" in s:          base -= 8
    if "preview" in s:      base -= 5
    if "thinking" in s:     base += 2
    return base

def list_available_models(provider, key, force=False):
    """Return a sorted list of (display_label, model_id) for the selectbox.
    Best/newest model is first. Results are cached in session_state.
    Falls back to a short hardcoded list if the API call fails.
    """
    cache = st.session_state.setdefault("model_list_cache", {})
    ck = f"{provider}::{_key_fp(key)}"
    if not force and ck in cache:
        return cache[ck]

    pairs = []   # list of (score, label, model_id)
    try:
        if provider == "Claude (Anthropic)":
            import anthropic
            c = anthropic.Anthropic(api_key=key)
            resp = c.models.list(limit=100)
            for m in resp.data:
                mid = m.id
                if "claude" not in mid.lower():
                    continue
                sk = _claude_sort_key(mid)
                ml = mid.lower()
                if "opus"   in ml: tag = "🔶 Opus"
                elif "sonnet" in ml: tag = "🔷 Sonnet"
                elif "haiku"  in ml: tag = "🔹 Haiku"
                else: tag = "◾"
                label = f"{tag} · {mid}"
                pairs.append((sk, label, mid))
            pairs.sort(key=lambda x: x[0], reverse=True)

        elif provider == "OpenAI":
            from openai import OpenAI
            c = OpenAI(api_key=key)
            resp = c.models.list()
            for m in resp.data:
                mid = m.id
                sc = _openai_score(mid)
                if sc < 0:
                    continue
                ml = mid.lower()
                if re.match(r'^o[0-9]', ml):   tag = "🟠 Reasoning"
                elif "gpt-5" in ml:             tag = "🔴 GPT-5"
                elif "gpt-4o" in ml:            tag = "🔷 GPT-4o"
                elif "gpt-4" in ml:             tag = "🔹 GPT-4"
                elif "gpt-3" in ml:             tag = "◾ GPT-3.5"
                else:                           tag = "◾"
                label = f"{tag} · {mid}"
                pairs.append(((sc,), label, mid))
            pairs.sort(key=lambda x: x[0], reverse=True)

        elif provider == "Gemini (Google)":
            import google.generativeai as genai
            genai.configure(api_key=key)
            models = list(genai.list_models())
            for m in models:
                if "generateContent" not in getattr(m, "supported_generation_methods", []):
                    continue
                n = m.name.split("/")[-1] if "/" in m.name else m.name
                sc = _gemini_score(n)
                if sc < 0:
                    continue
                nl = n.lower()
                if "pro" in nl:        tag = "🔶 Pro"
                elif "flash-lite" in nl: tag = "🔹 Flash-Lite"
                elif "flash" in nl:    tag = "🔷 Flash"
                else:                  tag = "◾"
                label = f"{tag} · {n}"
                pairs.append(((sc,), label, n))
            pairs.sort(key=lambda x: x[0], reverse=True)

    except Exception:
        pass   # fall through to hardcoded fallback

    if not pairs:
        # Hardcoded fallback — better than an empty picker
        fallback = {
            "Claude (Anthropic)": [
                ("🔶 Opus   · claude-opus-4-5",      "claude-opus-4-5"),
                ("🔷 Sonnet · claude-sonnet-4-5",    "claude-sonnet-4-5"),
                ("🔹 Haiku  · claude-haiku-4-5",     "claude-haiku-4-5"),
            ],
            "OpenAI": [
                ("🔷 GPT-4o · gpt-4o",               "gpt-4o"),
                ("🟠 o3    · o3",                     "o3"),
                ("🔹 GPT-4o · gpt-4o-mini",          "gpt-4o-mini"),
                ("◾ GPT-3.5 · gpt-3.5-turbo",        "gpt-3.5-turbo"),
            ],
            "Gemini (Google)": [
                ("🔶 Pro   · gemini-2.5-pro",         "gemini-2.5-pro"),
                ("🔷 Flash · gemini-2.0-flash",       "gemini-2.0-flash"),
                ("🔹 Flash · gemini-1.5-flash",       "gemini-1.5-flash"),
            ],
        }
        pairs = [(None, lbl, mid) for lbl, mid in fallback.get(provider, [])]

    result = [(lbl, mid) for _, lbl, mid in pairs]
    cache[ck] = result
    return result

def resolve_latest_model(provider, key, force=False):
    """Return just the model_id of the top-ranked model (first in list)."""
    models = list_available_models(provider, key, force=force)
    # Also keep backward-compat cache for call_llm fallback
    cache = st.session_state.setdefault("model_cache", {})
    ck = f"{provider}::{_key_fp(key)}"
    top = models[0][1] if models else {
        "Claude (Anthropic)": "claude-opus-4-5",
        "OpenAI":             "gpt-4o",
        "Gemini (Google)":    "gemini-2.0-flash",
    }.get(provider, "")
    cache[ck] = top
    return top

def _active_model(provider, key):
    """Always return the auto-detected best available model for the provider."""
    return resolve_latest_model(provider, key)

def call_llm(provider, key, system, user_msg, max_tokens=4096):
    model = _active_model(provider, key)
    if provider == "Claude (Anthropic)":
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        r = c.messages.create(model=model, max_tokens=max_tokens, system=system,
                              messages=[{"role": "user", "content": user_msg}])
        return r.content[0].text
    elif provider == "OpenAI":
        from openai import OpenAI
        c = OpenAI(api_key=key)
        # max_completion_tokens is supported by ALL OpenAI models (gpt-4o, o-series, etc.)
        # o-series also does NOT support a system role — merge it into the user message.
        is_o_series = bool(re.match(r'^o\d', model.lower()))
        if is_o_series:
            merged = f"{system}\n\n{user_msg}" if system else user_msg
            msgs = [{"role": "user", "content": merged}]
        else:
            msgs = ([{"role": "system", "content": system}] if system else [])
            msgs.append({"role": "user", "content": user_msg})
        r = c.chat.completions.create(model=model, messages=msgs,
                                      max_completion_tokens=max_tokens)
        return r.choices[0].message.content
    elif provider == "Gemini (Google)":
        import google.generativeai as genai
        genai.configure(api_key=key)
        m = genai.GenerativeModel(model)
        r = m.generate_content(f"[System]\n{system}\n\n[User]\n{user_msg}",
            generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens))
        return r.text
    raise ValueError(f"Unknown: {provider}")

def call_llm_multi(provider, key, system, messages, max_tokens=1024):
    model = _active_model(provider, key)
    if provider == "Claude (Anthropic)":
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        r = c.messages.create(model=model, max_tokens=max_tokens, system=system, messages=messages)
        return r.content[0].text
    elif provider == "OpenAI":
        from openai import OpenAI
        c = OpenAI(api_key=key)
        is_o_series = bool(re.match(r'^o\d', model.lower()))
        if is_o_series:
            flat = []
            if system:
                flat.append({"role": "user", "content": system})
                flat.append({"role": "assistant", "content": "Understood."})
            flat.extend(messages)
            msgs = flat
        else:
            msgs = ([{"role": "system", "content": system}] if system else []) + messages
        r = c.chat.completions.create(model=model, messages=msgs,
                                      max_completion_tokens=max_tokens)
        return r.choices[0].message.content
    elif provider == "Gemini (Google)":
        import google.generativeai as genai
        genai.configure(api_key=key)
        m = genai.GenerativeModel(model)
        conv = f"[System]\n{system}\n\n"
        for msg in messages:
            conv += f"[{'User' if msg['role'] == 'user' else 'Assistant'}]\n{msg['content']}\n\n"
        r = m.generate_content(conv, generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens))
        return r.text
    raise ValueError(f"Unknown: {provider}")

# ── Antibiotic line detection helper ─────────────────────────
# Matches patterns like:
#   "Tazocin (2026/04/22-)"
#   "Ceftriaxone (D1: 2025/01/15)"
#   "Vancomycin (2025/01/15-)"
#   "Piperacillin/Tazobactam (2025-01-15 - )"
_ABX_DATE_RE = re.compile(
    r'^[A-Z][A-Za-z/\-]+(?:\s*\+\s*[A-Z][A-Za-z/\-]+)?'
    r'\s*\([^)]*\d{4}[/\-]\d{1,2}[/\-]\d{1,2}[^)]*\)\s*$'
)

def _looks_like_antibiotic_line(stripped):
    """Does this line look like just 'Drugname (YYYY/MM/DD-)'?"""
    return bool(_ABX_DATE_RE.match(stripped))

def normalize_bullets(text, section_title=""):
    """Post-process bullet formatting.
    Plan: ensure Diagnostic/Therapeutic/Measurable goal sub-items use '- '.
    Impression: FLATTEN nested sub-items into parent numbered line (semicolon join);
                ensure <Underlying status> uses '- ' with no blank lines."""
    lines = text.split('\n')
    out = []
    in_plan_subsection = False
    in_underlying = False

    for line in lines:
        stripped = line.strip()

        # ── Plan sub-section handling ──
        if "Plan" in section_title:
            if re.match(r'^(Diagnostic|Therapeutic|Measurable\s+goal)\s*:', stripped, re.IGNORECASE):
                in_plan_subsection = True
                out.append(stripped)
                continue
            if in_plan_subsection:
                if not stripped:
                    out.append(line)
                    continue
                # Already correct " - " format
                if line.startswith(' - '):
                    out.append(line)
                    continue
                # Strip any existing bullet prefix and re-format as " - "
                # Match: "- text", "* text", "• text", "· text", "– text"
                m = re.match(r'^[\s]*[-•\*·–]\s*(.*)', stripped)
                if m:
                    out.append(' - ' + m.group(1))
                    continue
                # Match: numbered items "1. text", "2) text"
                m2 = re.match(r'^[\d]+[.)]\s*(.*)', stripped)
                if m2:
                    out.append(' - ' + m2.group(1))
                    continue
                # New sub-section header → reset
                if re.match(r'^(Diagnostic|Therapeutic|Measurable\s+goal)\s*:', stripped, re.IGNORECASE):
                    out.append(stripped)
                    continue
                # Plain text line → convert to " - "
                out.append(' - ' + stripped)
                continue

        # ── Impression handling ──
        if "Impression" in section_title:
            # Detect <Underlying status> boundary
            if '<Underlying status>' in stripped or '&lt;Underlying status&gt;' in stripped or 'Underlying status' in stripped:
                in_underlying = True
                out.append(stripped)
                continue

            if in_underlying:
                # Inside Underlying status: force " - " bullets, no blank lines
                if not stripped:
                    continue
                if line.startswith(' - '):
                    out.append(line)
                    continue
                # Strip "- " at start (no leading space)
                if stripped.startswith('- '):
                    out.append(' - ' + stripped[2:])
                    continue
                m = re.match(r'^[\s]*[•\*·–]\s*(.*)', stripped)
                if m:
                    out.append(' - ' + m.group(1))
                    continue
                m2 = re.match(r'^[\d]+[.)]\s*(.*)', stripped)
                if m2:
                    out.append(' - ' + m2.group(1))
                    continue
                out.append(' - ' + stripped)
                continue
            else:
                # Before Underlying status: convert ALL items to " - " format,
                # EXCEPT antibiotic sub-lines which should be 3-space indented.

                # Already correctly 3-space-indented antibiotic line? keep it
                if (line.startswith('   ') and not line.startswith(' - ')
                        and stripped and _looks_like_antibiotic_line(stripped)):
                    out.append('   ' + stripped)
                    continue

                # Already correct " - " format
                if line.startswith(' - '):
                    out.append(line)
                    continue
                # Numbered line (1. text) → convert to " - text"
                m_num = re.match(r'^\d+[.)]\s*(.*)', stripped)
                if m_num:
                    out.append(' - ' + m_num.group(1))
                    continue
                # "- text" at line start (no leading space) → convert
                if stripped.startswith('- '):
                    content = stripped[2:]
                    # If it's a pure antibiotic line under a prior diagnosis → indent sub-line
                    if _looks_like_antibiotic_line(content) and out and any(
                        o.startswith(' - ') for o in out
                    ):
                        out.append('   ' + content)
                    else:
                        out.append(' - ' + content)
                    continue
                # Indented or bullet sub-item → antibiotic sub-line OR semicolon-merge
                is_sub = False
                sub_content = stripped
                m_sub = re.match(r'^[\s]*[-•\*·–]\s*(.*)', stripped)
                if m_sub:
                    is_sub = True
                    sub_content = m_sub.group(1)
                elif line != line.lstrip() and stripped:
                    is_sub = True
                    sub_content = stripped

                if is_sub and out:
                    # If sub is an antibiotic line → 3-space-indented sub-line
                    if _looks_like_antibiotic_line(sub_content):
                        out.append('   ' + sub_content)
                        continue
                    # Otherwise preserve the legacy behavior: merge onto previous diagnosis via ';'
                    for j in range(len(out) - 1, -1, -1):
                        if out[j].startswith(' - '):
                            out[j] = out[j].rstrip() + '; ' + sub_content
                            break
                    continue

                # Blank lines → keep
                if not stripped:
                    out.append(line)
                    continue

                # Standalone antibiotic line (not indented, not bulleted) appearing after a diagnosis
                # → treat as indented sub-line
                if _looks_like_antibiotic_line(stripped) and out and any(
                    o.startswith(' - ') for o in out
                ):
                    out.append('   ' + stripped)
                    continue

                out.append(line)
                continue

        # ── General bullet normalization ──
        m = re.match(r'^[\s]*[•\*·–]\s*(.*)', stripped)
        if m:
            out.append(' - ' + m.group(1))
        else:
            out.append(line)

    # Remove blank lines between consecutive bullet-ish lines (compact).
    # Both " - " bullets and 3-space-indented antibiotic lines count as bullet-ish.
    def _is_bulletish(s):
        return s.startswith(' - ') or (s.startswith('   ') and not s.startswith('    '))
    result = []
    for i, line in enumerate(out):
        if line.strip() == '' and 0 < i < len(out) - 1:
            if _is_bulletish(out[i-1]) and _is_bulletish(out[i+1]):
                continue
        result.append(line)
    # Strip trailing spaces from each line (preserve leading indent)
    result = [l.rstrip() for l in result]
    return '\n'.join(result)

def render_card(idx, title, body):
    """Render a clean section card."""
    if body:
        # Normalize bullets for Plan and Impression
        if "Plan" in title or "Impression" in title:
            body = normalize_bullets(body, section_title=title)
    # Use hl_plain for Plan/Impression to prevent Markdown interpretation
    if body and ("Plan" in title or "Impression" in title):
        hi_body = hl_plain(body)
    else:
        hi_body = hl(body) if body else ""
    st.markdown(f'<div class="note-card">'
                f'<div class="nc-title">{html_lib.escape(title)}</div>'
                f'{hi_body}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""<div class="header-banner">
<h1>🏥 學習病歷產生器</h1>
<p>貼入病患資訊（門診紀錄 / 急診紀錄 / 標準化病人腳本），自動產生結構化學習病歷 · 學習重點 · AI 問答</p>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔑 API Key")
    st.caption("輸入任一即可 · 優先順序：Anthropic → OpenAI → Gemini")
    ka = st.text_input("Anthropic API Key", type="password", key="ka")
    ko = st.text_input("OpenAI API Key", type="password", key="ko")
    kg = st.text_input("Gemini API Key", type="password", key="kg")
    provider, active_key = detect_provider(ka, ko, kg)
    if provider:
        st.success(f"✅ 使用：{provider}", icon="🤖")
        # Auto-detect and show the model being used (no manual picker)
        try:
            auto_model = resolve_latest_model(provider, active_key)
            if auto_model:
                st.markdown(
                    f'<div class="model-badge">🧠 自動選用最新模型<br>'
                    f'<code style="color:#4A6480">{html_lib.escape(auto_model)}</code></div>',
                    unsafe_allow_html=True,
                )
        except Exception:
            pass
    else:
        st.info("請輸入至少一組 API Key")
    st.markdown("---")
    st.markdown("### 🎨 功能導覽")
    st.markdown(
        '<div style="font-size:.78rem;color:#5A6A7A;line-height:1.7">'
        '🚑 <b>急診 / 門診</b> 模式切換<br>'
        '🩸 檢驗分類輸入（血液 / 生化 / 其他）<br>'
        '📝 分段病歷 · 📏 精簡版 · 🔄 單段重生<br>'
        '📚 學習重點 + EBM 查核<br>'
        '💬 AI 多輪問答<br>'
        '🛡️ 自動去識別化<br>'
        '🔴 ROS/PE 紅字 · 🔵 補充資料藍字<br>'
        '💊 抗生素自動縮排標示'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Session State ───────────────────────────────────────────
for _k, _v in [("result", ""), ("learning", ""), ("chat_history", []),
               ("sections_data", []), ("variants", {})]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ══════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════
col_in, col_out = st.columns([2, 3], gap="large")

with col_in:
    st.markdown('<div class="section-label">📋 貼入病患資料</div>', unsafe_allow_html=True)
    st.markdown("""<div class="safety-warning">
⚠️ <b>請勿輸入可識別之病人個資</b>（姓名、身分證字號、電話等）<br>
⚠️ <b>本工具僅供教學用途</b>，不可用於真實臨床決策</div>""", unsafe_allow_html=True)

    # ── 入院來源（NEW）──
    admission_source_ui = st.radio(
        "🚪 入院來源",
        options=["🚑 急診入院", "🏥 門診入院"],
        index=0,
        horizontal=True,
        help="影響 Present Illness 寫法：急診會寫 At triage + vital signs + ER course；門診則以主訴 → OPD 檢查 → 建議住院為主軸，不寫 ER 內容",
    )
    admission_source = "OPD" if "門診" in admission_source_ui else "ER"

    # ── Age & Gender ──
    ag1, ag2 = st.columns(2)
    with ag1:
        patient_age = st.number_input("🎂 年齡", min_value=0, max_value=150, value=None,
                                       step=1, placeholder="e.g. 65", help="留空則由 AI 從資料推斷")
    with ag2:
        patient_gender = st.selectbox("⚧ 性別", options=["（自動推斷）", "male", "female"], index=0)

    patient_data = st.text_area(
        "主要資料",
        height=220,
        placeholder=(
            "貼入門診紀錄 / 急診紀錄 / SP 腳本...\n"
            "若急診紀錄含會診回覆，系統會自動把會診的 Impression 採為主診斷，"
            "並把會診建議（不加「Per X consult:」前綴）整入 Plan。"
        ),
        label_visibility="collapsed",
    )

    # ── 檢驗結果分三欄（NEW）──
    st.markdown(
        '<div style="font-size:.88rem;font-weight:600;color:#4A6480;'
        'margin:.4rem 0 .2rem;letter-spacing:.02em">🔬 檢驗結果（選填）</div>',
        unsafe_allow_html=True,
    )
    lab_blood = st.text_area(
        "🩸 血液檢驗",
        height=75,
        placeholder="CBC, DC, Coagulation (PT / aPTT / INR), Reticulocyte...",
        help="血液常規、分類計數、凝血功能",
    )
    lab_biochem = st.text_area(
        "🧪 生化檢驗",
        height=75,
        placeholder="Liver / Renal function, Electrolytes, CRP, Procalcitonin, Troponin, BNP, Lactate, ABG...",
        help="肝腎功能、電解質、發炎指標、心臟標記、血糖血脂、動脈血氣",
    )
    lab_other = st.text_area(
        "🔬 其他檢驗",
        height=75,
        placeholder="Urinalysis, Microbiology culture (blood / urine / sputum), EKG, CXR, CT, Echo, Pathology...",
        help="尿液、微生物培養、心電圖、影像、病理等其他檢查",
    )

    past_hx_input = st.text_area("📄 過去出院診斷 / ER 診斷（選填）", height=85,
        placeholder="原樣保留貼入內容（條列或編號皆可），作為 Past History 主要來源...")

    supplement = st.text_area("📝 補充資料（選填）", height=80,
        placeholder="後續問診結果、額外病史等（中英文皆可，於 PI 以藍字標示）...")

    st.markdown("""<div class="tips-box">
💡 所有欄位合併生成。🔴 ROS/PE 更動以<span style="color:#FF6B6B;font-weight:700;">紅字</span>、<span style="color:#FF6B6B;font-weight:700;">*</span> 前綴標示異常。
🔵 補充資料於 PI 以<span style="color:#4A6480;font-weight:700;">藍字</span>顯示。🛡️ 姓名/身分證/電話自動去識別化。
📄 過去出院診斷會「原樣保留」於 Past History，並自動摘入 PI underlying 與 Impression。
🩺 會診回覆：其 impression → 當主診斷；其建議 → 整入 Plan（不加來源標籤）。
💊 抗生素自動於 Impression 主診斷下方縮排顯示：<code style="color:#FF6B6B">Tazocin (2026/04/22-)</code>
</div>""", unsafe_allow_html=True)

    btn1, btn2 = st.columns(2)
    with btn1:
        gen_med = st.button("🩺 產生學習病歷", use_container_width=True)
    with btn2:
        gen_surg = st.button("🔪 產生外科病歷", use_container_width=True)

    if gen_med or gen_surg:
        surgical = gen_surg
        if not active_key:
            st.warning("請先輸入至少一組 API Key。")
        elif not patient_data.strip():
            st.error("請貼入病患資料。")
        else:
            st.session_state.update({
                "result": "", "learning": "", "chat_history": [],
                "sections_data": [], "variants": {},
            })
            combined = anonymize(patient_data.strip())

            # Categorized exam blocks — each labeled so the prompt can identify category
            if lab_blood.strip():
                combined += "\n\n--- 血液檢驗 ---\n" + anonymize(lab_blood.strip())
            if lab_biochem.strip():
                combined += "\n\n--- 生化檢驗 ---\n" + anonymize(lab_biochem.strip())
            if lab_other.strip():
                combined += "\n\n--- 其他檢驗 ---\n" + anonymize(lab_other.strip())

            if past_hx_input.strip():
                combined += "\n\n--- 過去出院診斷 ---\n" + anonymize(past_hx_input.strip())
            if supplement.strip():
                combined += "\n\n--- 補充資料 ---\n" + anonymize(supplement.strip())

            # Prepend admission-source hint so the model definitely sees it
            source_hint = (
                "【入院來源】急診入院 (ER admission) — 請依 ER 風格寫 PI（含 At triage + vital signs + ER course）\n\n"
                if admission_source == "ER"
                else "【入院來源】門診入院 (OPD admission) — 直接從門診收住院，請依 OPD 風格寫 PI（主訴 → OPD 檢查 → 建議住院原因），不要寫 ER course\n\n"
            )
            combined = source_hint + combined

            gender_val = patient_gender if patient_gender != "（自動推斷）" else None
            sys_prompt = build_system_prompt(
                surgical=surgical,
                age=patient_age,
                gender=gender_val,
                past_hx=past_hx_input.strip(),
                admission_source=admission_source,
            )
            label_type = "外科" if surgical else "內科"
            label_src = "急診" if admission_source == "ER" else "門診"

            with st.spinner(f"使用 {provider} 生成 {label_src}{label_type}病歷⋯"):
                try:
                    st.session_state["result"] = call_llm(provider, active_key, sys_prompt, combined)
                except Exception as e:
                    st.error(f"錯誤：{e}")

            if st.session_state["result"]:
                st.rerun()

# ── RIGHT ───────────────────────────────────────────────────
with col_out:
    if st.session_state["result"]:
        tab_note, tab_learn, tab_chat = st.tabs(["📝 學習病歷", "📚 學習重點", "💬 AI 問答"])

        with tab_note:
            result = st.session_state["result"]
            # Clean download text
            clean_dl = re.sub(r'⚠\*\*(.+?)\*\*', r'*\1', result)  # ROS abnormal → *value
            clean_dl = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_dl)
            clean_dl = re.sub(r'\[\[(.+?)\]\]', r'\1', clean_dl)
            clean_dl = clean_dl.replace("===SECTION===", "").strip()
            # Normalize Plan/Impression bullet format in download text
            dl_sections = parse_sections(result)
            if dl_sections:
                for _t, _b in dl_sections:
                    if ("Plan" in _t or "Impression" in _t) and _b:
                        normalized_b = normalize_bullets(_b, section_title=_t)
                        # Also clean markers for download
                        clean_b = re.sub(r'⚠\*\*(.+?)\*\*', r'*\1', _b)
                        clean_b = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_b)
                        clean_nb = re.sub(r'⚠\*\*(.+?)\*\*', r'*\1', normalized_b)
                        clean_nb = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_nb)
                        if clean_b in clean_dl:
                            clean_dl = clean_dl.replace(clean_b, clean_nb)
            # Strip trailing spaces from each line in download
            clean_dl = '\n'.join(l.rstrip() for l in clean_dl.split('\n'))
            st.download_button("📥 下載完整病歷 (.txt)", data=clean_dl,
                               file_name="medical_note.txt", mime="text/plain", use_container_width=True)
            st.markdown('<div style="font-size:.74rem;color:#95a5a6;margin-bottom:.3rem">'
                        '🔴 紅色=ROS/PE更動 ｜ *=ROS異常提示 ｜ 🔵 藍色=補充資料內容 ｜ 📏=精簡版（PI·Imp·Plan）</div>',
                        unsafe_allow_html=True)

            if not st.session_state["sections_data"]:
                st.session_state["sections_data"] = parse_sections(result)
            sections = st.session_state["sections_data"]
            VARIANT_OK = {"現在病症 (Present Illness)", "臨床臆斷 (Impression)", "處理計畫 (Plan)"}

            if not sections:
                st.markdown(f'<div class="note-card">{hl(result)}</div>', unsafe_allow_html=True)
            else:
                for idx, (title, body) in enumerate(sections):
                    render_card(idx, title, body)

                    if title in VARIANT_OK:
                        if st.button("📏 精簡版", key=f"sh_{idx}"):
                            if active_key:
                                with st.spinner("生成精簡版⋯"):
                                    try:
                                        p = VARIANT_PROMPT.format(full_note=result,
                                                                  section_title=title, original_content=body)
                                        t = call_llm(provider, active_key, "", p, max_tokens=2048)
                                        v = dict(st.session_state["variants"])
                                        v.setdefault(idx, {})["short"] = t.strip()
                                        st.session_state["variants"] = v
                                    except Exception as e:
                                        st.error(str(e))
                                st.rerun()

                    sv = st.session_state["variants"].get(idx, {})
                    if "short" in sv:
                        short_body = sv["short"]
                        if "Plan" in title or "Impression" in title:
                            short_body = normalize_bullets(short_body, section_title=title)
                            short_html = hl_plain(short_body)
                        else:
                            short_html = hl(short_body)
                        st.markdown(f'<div class="variant-label">📏 精簡版</div>'
                                    f'<div class="variant-card">{short_html}</div>',
                                    unsafe_allow_html=True)

        with tab_learn:
            st.markdown('<div class="section-label-green">📚 臨床學習重點</div>', unsafe_allow_html=True)
            if st.session_state["learning"]:
                st.download_button("📥 下載學習重點 (.txt)",
                                   data=st.session_state["learning"],
                                   file_name="learning_notes.txt", mime="text/plain",
                                   use_container_width=True)
                st.markdown(st.session_state["learning"])
            else:
                st.info("按下方按鈕生成學習重點（需額外 API token）。")
                if st.button("📚 生成學習重點", use_container_width=True, key="gen_learn"):
                    if active_key:
                        with st.spinner("生成學習重點⋯"):
                            try:
                                st.session_state["learning"] = call_llm(
                                    provider, active_key, LEARNING_ZONE_PROMPT,
                                    st.session_state["result"], max_tokens=3500)
                            except Exception:
                                st.session_state["learning"] = "（生成失敗，請重試）"
                        st.rerun()
                    else:
                        st.warning("請先輸入 API Key。")

        with tab_chat:
            st.markdown('<div class="section-label-purple">💬 病歷 AI 問答</div>', unsafe_allow_html=True)
            st.caption("例如：「病患有無發燒？」「為什麼選這個抗生素？」")
            if st.session_state["chat_history"]:
                parts = []
                for m in st.session_state["chat_history"]:
                    esc = html_lib.escape(m["content"])
                    cls = "chat-msg-user" if m["role"] == "user" else "chat-msg-ai"
                    parts.append(f'<div class="{cls}">{esc}</div>')
                st.markdown(f'<div class="chat-container">{"".join(parts)}</div>', unsafe_allow_html=True)

            ci = st.text_input("提問", placeholder="輸入問題⋯", key="ci", label_visibility="collapsed")
            c1, c2 = st.columns([3, 1])
            with c1:
                send = st.button("送出", use_container_width=True, key="send")
            with c2:
                if st.button("清除", use_container_width=True, key="clr"):
                    st.session_state["chat_history"] = []
                    st.rerun()
            if send and ci.strip() and active_key:
                st.session_state["chat_history"].append({"role": "user", "content": ci.strip()})
                sys = CHAT_SYSTEM_PROMPT.format(note=st.session_state["result"])
                msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state["chat_history"]]
                with st.spinner("⋯"):
                    try:
                        ans = call_llm_multi(provider, active_key, sys, msgs)
                        st.session_state["chat_history"].append({"role": "assistant", "content": ans})
                    except Exception as e:
                        st.session_state["chat_history"].append({"role": "assistant", "content": f"錯誤：{e}"})
                st.rerun()
    else:
        st.markdown("""<div class="empty-placeholder">
<div style="font-size:3rem;margin-bottom:.6rem;opacity:.6">📄</div>
<div style="font-size:1rem;font-weight:500;color:#4A6480">產生的學習病歷將顯示在此處</div>
<div style="font-size:.85rem;margin-top:.5rem;color:rgba(160,190,230,.75)">請先在左側選擇入院來源並貼入資料，按下按鈕開始生成</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""<div class="footer-disclaimer">
⚠️ <b>免責聲明</b><br>
本工具僅供醫學教育與學習用途，不應用於實際臨床診療決策。使用者需自行判斷其正確性。<br>
使用第三方 AI API（Anthropic / OpenAI / Google），使用者需自行負責 API token 消耗與相關費用。</div>""", unsafe_allow_html=True)
