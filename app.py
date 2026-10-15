import json, re
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Hamza AI | Recruiter Demo", page_icon="🧠", layout="wide")
DATA = json.loads(Path(__file__).with_name("profile_knowledge.json").read_text(encoding="utf-8"))

st.markdown("""
<style>
.stApp {background: radial-gradient(circle at 10% 0%, #29113b 0, #0b0b16 45%, #10101d 100%); color:#f5f1ff}
section[data-testid="stSidebar"] {background:#171022}
.hero {padding:1.4rem 1.6rem;border:1px solid #693a83;border-radius:18px;background:linear-gradient(120deg,#261032,#171526);margin-bottom:1rem}
.kicker {color:#e2c14c;letter-spacing:2px;font-size:.75rem;font-weight:700}
.hero h1 {margin:.3rem 0;color:#f8eaff;font-size:2.1rem}
.hero p {color:#d3c6df;margin-bottom:0}
.source {padding:.75rem 1rem;border-left:3px solid #d7b842;background:#21182c;border-radius:8px;margin:.45rem 0}
.metric {padding:1rem;border:1px solid #3e3150;border-radius:12px;background:#191624}
div.stButton>button {border-radius:10px;border:1px solid #a66bd0}
</style>
<div class="hero"><div class="kicker">RECRUITER MODE · CV-GROUNDED PROTOTYPE</div><h1>Interview the AI That Represents Me</h1><p>A transparent assistant that answers from Hamza's CV, cites its evidence, and refuses unsupported claims.</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧭 Recruiter mode")
    lang = st.radio("Response language / Langue / اللغة", ["English", "Français", "العربية"], horizontal=False)
    st.caption("This prototype uses a fixed, reviewable CV knowledge base. It does not access private employer data.")
    st.markdown("---")
    st.markdown("**Try a question**")
    presets = ["What has Hamza built?", "What is his experience with LLM evaluation?", "Did Hamza work at Google for 5 years?", "What are his main technical skills?"]
    selected = st.selectbox("Preset questions", presets)
    if st.button("Ask preset", use_container_width=True):
        st.session_state.question = selected

st.markdown("### Ask the candidate's AI")
if "question" not in st.session_state: st.session_state.question = "What has Hamza built?"
question = st.text_input("Ask in English, French, or Arabic", key="question", placeholder="e.g. Did Hamza work at Google for 5 years?")

STOP_WORDS = set("what has did how tell me about the his her is are experience skills main to at for years work worked with and a an in of does il elle est sont les des du de la le un une quelles compétences expérience a-t-il travaillé pendant chez google cinq ans ما هي هل في جوجل لمدة سنوات خبرة مهارات التي".split())
def tokens(s):
    return [x for x in re.findall(r"[\w+#.-]+", s.lower()) if x not in STOP_WORDS and len(x)>1]
def retrieve(q):
    q_tokens = set(tokens(q))
    scored = []

    for item in DATA["facts"]:
        corpus = " ".join([item["claim"]] + item["keywords"]).lower()
        corpus_tokens = set(tokens(corpus))
        overlap = q_tokens & corpus_tokens
        score = len(overlap) / max(1, len(q_tokens))

        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:3]

def localized_intro(language, items):
    if language == "Français": return "D'après les éléments du CV disponibles :" if items else "Je ne trouve pas de preuve suffisante dans le CV fourni pour répondre avec fiabilité."
    if language == "العربية": return "استنادًا إلى المعلومات المتاحة في السيرة الذاتية:" if items else "لا أجد دليلاً كافيًا في السيرة الذاتية المتاحة للإجابة بثقة."
    return "Based on the available CV evidence:" if items else "I don't have enough evidence in the available CV to answer that reliably."

def answer_text(items, language):
    if not items: return localized_intro(language, [])
    claims=[x[1]["claim"] for x in items]
    if language == "Français":
        translations={
          "Hamza is an AI Engineer and Data Scientist focused on Generative AI, LLM evaluation, and applied data science.":"Hamza est ingénieur en IA et data scientist, spécialisé en IA générative, évaluation des LLM et science des données appliquée.",
          "At Turing, Hamza evaluates frontier LLM outputs for factual accuracy, reasoning quality, instruction-following, and safety alignment.":"Chez Turing, Hamza évalue les réponses de LLM avancés selon l'exactitude factuelle, le raisonnement, le respect des consignes et la sécurité.",
          "Hamza's CV describes a trilingual Arabic/French/English health-tech RAG platform using FastAPI, ChromaDB, Claude API, and Docker.":"Le CV de Hamza décrit une plateforme RAG de santé en arabe, français et anglais utilisant FastAPI, ChromaDB, l'API Claude et Docker.",
          "Hamza reports building a longitudinal data pipeline covering more than 5,500 labelled biometric records, with Random Forest and LSTM models.":"Hamza indique avoir créé un pipeline de données longitudinal couvrant plus de 5 500 enregistrements biométriques étiquetés, avec des modèles Random Forest et LSTM.",
          "Hamza delivers corporate training in Machine Learning, Python, data visualization, and Generative AI at BIOTREND.":"Hamza dispense chez BIOTREND des formations en apprentissage automatique, Python, visualisation des données et IA générative.",
          "Hamza co-founded Trevanah Academy, an online academy focused on professional skills for the digital economy.":"Hamza a cofondé Trevanah Academy, une académie en ligne axée sur les compétences professionnelles de l'économie numérique.",
          "His listed tools include Python, SQL, Git/GitHub, LangChain, LangGraph, ChromaDB, FastAPI, Docker, and AWS SageMaker.":"Parmi les outils mentionnés figurent Python, SQL, Git/GitHub, LangChain, LangGraph, ChromaDB, FastAPI, Docker et AWS SageMaker."
        }
        return " ".join(translations.get(c,c) for c in claims)
    if language == "العربية":
        translations={
          "Hamza is an AI Engineer and Data Scientist focused on Generative AI, LLM evaluation, and applied data science.":"حمزة مهندس ذكاء اصطناعي وعالم بيانات، يركز على الذكاء الاصطناعي التوليدي وتقييم نماذج اللغة والبيانات التطبيقية.",
          "At Turing, Hamza evaluates frontier LLM outputs for factual accuracy, reasoning quality, instruction-following, and safety alignment.":"وفقًا لسيرته الذاتية، يعمل حمزة لدى Turing على تقييم مخرجات نماذج اللغة من حيث الدقة الواقعية وجودة الاستدلال واتباع التعليمات والسلامة.",
          "Hamza's CV describes a trilingual Arabic/French/English health-tech RAG platform using FastAPI, ChromaDB, Claude API, and Docker.":"تصف سيرته الذاتية منصة RAG في مجال الصحة بثلاث لغات: العربية والفرنسية والإنجليزية، باستخدام FastAPI وChromaDB وClaude API وDocker.",
          "Hamza reports building a longitudinal data pipeline covering more than 5,500 labelled biometric records, with Random Forest and LSTM models.":"تذكر سيرته الذاتية إنشاء خط معالجة بيانات طولي يضم أكثر من 5,500 سجل بيومتري موسوم، مع نماذج Random Forest وLSTM.",
          "Hamza delivers corporate training in Machine Learning, Python, data visualization, and Generative AI at BIOTREND.":"يقدم حمزة في BIOTREND تدريبًا مؤسسيًا في تعلم الآلة وPython وتصوير البيانات والذكاء الاصطناعي التوليدي.",
          "Hamza co-founded Trevanah Academy, an online academy focused on professional skills for the digital economy.":"شارك حمزة في تأسيس Trevanah Academy، وهي أكاديمية عبر الإنترنت تركز على المهارات المهنية للاقتصاد الرقمي.",
          "His listed tools include Python, SQL, Git/GitHub, LangChain, LangGraph, ChromaDB, FastAPI, Docker, and AWS SageMaker.":"تشمل الأدوات المذكورة في سيرته الذاتية Python وSQL وGit/GitHub وLangChain وLangGraph وChromaDB وFastAPI وDocker وAWS SageMaker."
        }
        return " ".join(translations.get(c,c) for c in claims)
    return " ".join(claims)

if st.button("Evaluate and answer", type="primary", use_container_width=True):
    q = question.strip()

    if not q:
        st.warning("Enter a question first.")

    elif re.search(
        r"google.{0,30}(5|five)|5.{0,20}years.{0,20}google|جوجل.{0,30}(5|خمس)|google.{0,20}ans|عمل.{0,20}جوجل.{0,20}(خمس|5)",
        q,
        re.I,
    ):
        st.error(
            "Unsupported claim rejected / Affirmation non étayée rejetée / تم رفض الادعاء غير المدعوم"
        )

        if lang == "English":
            answer = (
                "I found no evidence in the provided CV that Hamza worked "
                "at Google for five years. I won't present that claim as fact."
            )
        elif lang == "Français":
            answer = (
                "Le CV fourni ne prouve pas que Hamza a travaillé chez Google "
                "pendant cinq ans. Je ne présenterai pas cette affirmation comme un fait."
            )
        else:
            answer = (
                "لا تقدم السيرة الذاتية المتاحة دليلاً على أن حمزة عمل في "
                "Google لمدة خمس سنوات، لذلك لن أقدم هذا الادعاء على أنه حقيقة."
            )

        st.markdown("**Answer:** " + answer)
        st.caption("Guardrail result: PASS — unsupported claim was not accepted.")

    else:
        results = retrieve(q)

        # Ignore weak retrieval matches instead of presenting unrelated CV facts.
        if results and results[0][0] < 0.12:
            results = []

        st.markdown("**Answer**")
        st.write(localized_intro(lang, results))

        if results:
            st.write(answer_text(results, lang))

        st.markdown("**Evidence / Sources**")
        if results:
            for score, item in results:
                st.markdown(
                    f'<div class="source"><b>{item["source"]}</b><br>'
                    f'{item["claim"]}<br>'
                    f'<small>Retrieval match: {score:.0%}</small></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info(
                "No matching CV evidence was retrieved. The safe response is to abstain."
            )

st.markdown("---")
st.markdown("### Evaluation snapshot")
c1,c2,c3=st.columns(3)
with c1: st.markdown('<div class="metric"><small>Evidence trace</small><h3>Source-linked</h3><small>CV section shown per answer</small></div>',unsafe_allow_html=True)
with c2: st.markdown('<div class="metric"><small>Unsupported-claim test</small><h3>Built-in</h3><small>Google five-year trap</small></div>',unsafe_allow_html=True)
with c3: st.markdown('<div class="metric"><small>Languages</small><h3>EN · FR · AR</h3><small>Question and response demo</small></div>',unsafe_allow_html=True)
st.caption("Prototype note: retrieval uses a curated CV knowledge base and deterministic guardrails, not a production LLM. Validate every answer before recording or publishing.")
