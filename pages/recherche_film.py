import streamlit as st
import pandas as pd
import os
from app import afficher_barre_navigation, local_css, BASE_DIR

# TOUJOURS EN PREMIER
st.set_page_config(
    layout="wide",
    page_title="MOVIEDEN - Recherche de films",
    page_icon="🔍")

# CSS et navigation
local_css(os.path.join(BASE_DIR, "assets", "style.css"))
afficher_barre_navigation()

df_movies = pd.read_csv(os.path.join(BASE_DIR, "data", "df_film.csv"))


# Supporter l'ouverture d'un film depuis la page d'accueil via le paramètre URL `movie_id`
params = st.query_params
if 'movie_id' in params and 'selected_movie' not in st.session_state:
    try:
        movie_id_param = int(params['movie_id'][0])
        movie_row = df_movies[df_movies['id_tmdb'] == movie_id_param]
        if not movie_row.empty:
            st.session_state['selected_movie'] = movie_row.iloc[0].to_dict()
            # Nettoyer les query params pour éviter une boucle et recharger la page
            st.query_params = {}
            st.rerun()
    except Exception:
        pass


def parse_genres(val):
    if isinstance(val, list):
        return [str(g).strip() for g in val if str(g).strip()]
    if pd.isna(val) or val == '':
        return []
    if isinstance(val, str):
        val = val.strip()
        if val.startswith('[') and val.endswith(']'):
            try:
                parsed = eval(val)
                if isinstance(parsed, list):
                    return [str(g).strip() for g in parsed if str(g).strip()]
            except Exception:
                pass
        return [g.strip() for g in val.split(',') if g.strip()]
    return [str(val)]
all_genres = []
for genres in df_movies["genres"].dropna():
    all_genres.extend(parse_genres(genres))

# Supprimer les doublons et trier
all_genres = sorted(list(set(all_genres)))

def movie_has_genre(genres, selected_genre):
    try:
        genres_list = parse_genres(genres)
        return selected_genre in genres_list
    except:
        return False



# Titre
st.title("🔍 Recherche de films")

st.write("Recherchez vos films préférés")

# Barre de recherche
search = st.text_input(
    "Entrez un nom de film",
    placeholder="Exemple : Batman"
)
# Filtre genre
selected_genre = st.selectbox(
    "🎭 Filtrer par genre",
    ["Tous"] + all_genres
)
# Filtrage
results = df_movies.copy()

if search:
    title_fr_mask = results["title_fr"].fillna("").str.contains(search, case=False, na=False)
    primary_title_mask = results["primaryTitle"].fillna("").str.contains(search, case=False, na=False)
    results = results[title_fr_mask | primary_title_mask]

if selected_genre != "Tous":
    results = results[
        results["genres"].apply(
            lambda genres: selected_genre in genres
            if pd.notna(genres)
            else False
        )
    ]

# Afficher seulement si l'utilisateur a fait une recherche ou choisi un genre
if search or selected_genre != "Tous":

    st.write(f"{len(results)} résultat(s) trouvé(s)")

    
    source = "https://image.tmdb.org/t/p/original/"

# Pagination
films_par_page = 20

total_pages = (len(results) - 1) // films_par_page + 1

if "page" not in st.session_state:
    st.session_state["page"] = 1

col_prev, col_page, col_next = st.columns([1, 8.5, 1])

with col_prev:
    st.markdown("<div style='display:flex; justify-content:flex-end;'>", unsafe_allow_html=True)
    if st.button("⬅️ Précédent") and st.session_state["page"] > 1:
        st.session_state["page"] -= 1
        st.rerun()

with col_page:
    st.markdown(
        f"<h4 style='text-align:center;'>Page {st.session_state['page']} / {total_pages}</h4>",
        unsafe_allow_html=True
    )

with col_next:
    st.markdown("""
        <style>
        div[data-testid="column"]:last-child .stButton {
            display: flex;
            justify-content: flex-end;
        }
        </style>
    """, unsafe_allow_html=True)
    if st.button("Suivant ➡️") and st.session_state["page"] < total_pages:
        st.session_state["page"] += 1
        st.rerun()

page = st.session_state["page"]

start = (page - 1) * films_par_page
end = start + films_par_page

results_page = results.iloc[start:end]

st.write(f"Page {page} / {total_pages}")

cols = st.columns(5)

for index, (_, movie) in enumerate(results_page.iterrows()):

        with cols[index % 5]:
            source = "https://image.tmdb.org/t/p/original/"
            poster = f"{source}{movie.get('poster_path', '')}"

            genres = parse_genres(movie.get('genres', ''))
            genres_text = " • ".join(genres) if genres else ""

            title_card = movie.get('title_fr') or movie.get('primaryTitle') or movie.get('title', 'Titre inconnu')
            vote_card = movie.get('avg_rating_imdb') if pd.notna(movie.get('avg_rating_imdb')) else 0
            release_card = movie.get('startYear') or movie.get('release_date', 'N/A')

            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}">
                <div class="movie-title">{title_card}</div>
                <div class="movie-info">
                    ⭐ {vote_card:.1f}/10
                </div>
                <div class="movie-info">
                    📅 {release_card}
                </div>
                <div class="movie-info">
                    🎭 {genres_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "🎬 Voir détails",
                key=f"details_{index}"
            ):
                st.session_state["selected_tconst"] = movie["tconst"]
                st.switch_page("pages/movie_detail.py")
else:
    st.info("Tapez un titre ou choisissez un genre pour commencer la recherche.")
