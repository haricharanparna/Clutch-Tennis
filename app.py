# -----------------------------
# REVIEWS SECTION (HTML FIXED)
# -----------------------------
st.markdown(
    """
<div class="section-header">
    <div class="section-kicker">Testimonials</div>
    <div class="section-title">What Players Say</div>
</div>
""",
    unsafe_allow_html=True
)

if "review_page" not in st.session_state:
    st.session_state.review_page = 0

items_per_page = 3
total_pages = (len(reviews) + items_per_page - 1) // items_per_page

start_idx = st.session_state.review_page * items_per_page
current_reviews = reviews[start_idx:start_idx + items_per_page]

# Build clean HTML cards string
card_items = []
for rev in current_reviews:
    card_html = f"""
    <div class="review-card-slide">
        <div>
            <div class="review-stars">{rev['stars']}</div>
            <div class="review-text">"{rev['text']}"</div>
        </div>
        <div>
            <div class="review-author">{rev['author']}</div>
            <div class="review-role">{rev['role']}</div>
        </div>
    </div>
    """
    card_items.append(card_html)

# Wrap inside single container string
carousel_html = f'<div class="carousel-container">{"".join(card_items)}</div>'

st.markdown(carousel_html, unsafe_allow_html=True)

# Compact Pagination Dots Bar
st.markdown('<div class="dot-btn-container">', unsafe_allow_html=True)
nav_spacer_left, nav_center, nav_spacer_right = st.columns([3, 1, 3])

with nav_center:
    dot_cols = st.columns(total_pages)
    for page_num in range(total_pages):
        with dot_cols[page_num]:
            dot_symbol = "●" if page_num == st.session_state.review_page else "○"
            if st.button(dot_symbol, key=f"dot_page_{page_num}", use_container_width=True):
                st.session_state.review_page = page_num
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
