import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_app import load_data, filter_data

# Estilo personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #2E86AB 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .insight-box {
        background: linear-gradient(135deg, #1a3293 0%, #2E86AB 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">⭐ Dashboard de Avaliações - Análise de Satisfação</h1>', unsafe_allow_html=True)

df = load_data(file_path="book_rating_price.csv")
df_filtered = filter_data(rating=True, file_path="book_rating_price.csv")

def plot_bar_chart(data, x_col, y_col, title, x_label, y_label, orientation='h'):
    fig = px.bar(
        x=data[x_col] if orientation == 'v' else data[y_col],
        y=data[y_col] if orientation == 'v' else data[x_col],
        title=title,
        text=data[x_col].values.round(2) if orientation == 'h' else data[x_col].values.round(0).astype(int),
        labels={'x': x_label, 'y': y_label},
        orientation=orientation,
        color=data[x_col],
    )

    fig.update_layout(
        title_font_size=22,
        title_x=0.3,
        coloraxis_showscale=False  
    )

    st.plotly_chart(fig, use_container_width=True)

# Métricas gerais
col1, col2, col3, col4 = st.columns(4)
with col1:
    avg_rating = df['rating'].mean()
    st.metric("⭐ Avaliação Média", f"{avg_rating:.1f}/5", border=True)
with col2:
    total_reviews = len(df)
    st.metric("📝 Total de Avaliações", f"{total_reviews:,}", border=True)
with col3:
    avg_price = df['price'].mean()
    st.metric("💰 Preço Médio", f"R$ {avg_price:.2f}", border=True)
with col4:
    satisfaction_rate = len(df[df['rating'] >= 4]) / len(df) * 100
    st.metric("😊 Taxa de Satisfação", f"{satisfaction_rate:.1f}%", border=True)


if df_filtered.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados. Tente ajustar os filtros.")
else:

    # Análise principal
    st.markdown("## 📊 Análise de Preços por Avaliação")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            # Preço médio por avaliação
            df_filtered['rating'] = df_filtered['rating'].astype(int)
            avg_price_by_rating = df_filtered.groupby("rating")["price"].mean().sort_values(ascending=True)
            
            fig_price_rating = px.bar(
                x=avg_price_by_rating.values,
                y=[f"{int(i)} ⭐" for i in avg_price_by_rating.index],
                title="Preço Médio por Nível de Avaliação",
                text=avg_price_by_rating.values.round(2),
                labels={'x': 'Preço Médio (R$)', 'y': 'Avaliação'},
                orientation='h',
                color=avg_price_by_rating.values,
            )
            
            fig_price_rating.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_price_rating, use_container_width=True)

    with col2:
        with st.container(border=True):
            # Distribuição de avaliações
            rating_counts = df_filtered["rating"].value_counts().sort_index(ascending=True)
            
            fig_rating_dist = px.bar(
                x=rating_counts.values,
                y=[f"{int(i)} ⭐" for i in rating_counts.index],
                title="Distribuição de Avaliações",
                text=rating_counts.values,
                labels={'x': 'Quantidade de Avaliações', 'y': 'Avaliação'},
                orientation='h',
                color=rating_counts.values,
            )
            
            fig_rating_dist.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_rating_dist, use_container_width=True)

    # Insights sobre preços e avaliações
    st.markdown("""
    <div class="insight-box">
    <h3>🎯 Insights: Preço vs Avaliação</h3>
    <ul>
    <li><strong>Livros 5 estrelas</strong> apresentam preço médio menor (R$ 14,75), indicando que preços competitivos podem inflênciar as avaliações.</li>
    <li><strong>Concentração de Satisfação:</strong> Mais de 75% das avaliações (76.87%) são de 5 ou 4 estrelas, demonstrando alta qualidade dos produtos.</li>
    <li><strong>Estratégia:</strong> Promover livros bem avaliados destacando o valor superior pelo preço competitivo.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Análise por gênero
    st.markdown("## 📚 Análise de Satisfação por Gênero")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            # Avaliação média por gênero
            avg_rating_genre = df_filtered.groupby("genre_desc")["rating"].mean().sort_values(ascending=True)
            
            fig_genre_rating = px.bar(
                x=avg_rating_genre.values,
                y=avg_rating_genre.index,
                title="Avaliação Média por Gênero",
                text=avg_rating_genre.values.round(1),
                labels={'x': 'Avaliação Média', 'y': 'Gênero'},
                orientation='h',
                color=avg_rating_genre.values,
            )
            
            fig_genre_rating.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_genre_rating, use_container_width=True)

    with col2:
        with st.container(border=True):
            # Quantidade de avaliações por gênero
            reviews_by_genre = df_filtered["genre_desc"].value_counts().sort_values(ascending=True)
            
            fig_reviews_genre = px.bar(
                x=reviews_by_genre.values,
                y=reviews_by_genre.index,
                title="Quantidade de Avaliações por Gênero",
                text=reviews_by_genre.values,
                labels={'x': 'Quantidade de Avaliações', 'y': 'Gênero'},
                orientation='h',
                color=reviews_by_genre.values,
            )
            
            fig_reviews_genre.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_reviews_genre, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <h3>📚 Insights: Satisfação por Gênero</h3>
    <ul>
    <li><strong>Não Uniformidade de Qualidade:</strong> Genêro de Nonfiction tem avaliação média de 3.7 estrelas, indicando qualidade inconsistente. </li>
    <li><strong>SciFi/Fantasy Lidera:</strong> Gênero com maior volume de avaliações, confirmando popularidade.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Análise avançada
    st.markdown("## 🔍 Análise Avançada de Satisfação")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            # Distribuição de preços por faixa de avaliação
            # Criar uma coluna categórica para rating de 1 a 5
            df_filtered['rating_category'] = df_filtered['rating'].round().astype(int)
            
            # Garantir que todas as categorias de 1 a 5 existam
            df_filtered['rating_category'] = df_filtered['rating_category'].clip(1, 5)
            
            fig_price_dist = px.histogram(
                df_filtered,
                x="price",
                color="rating_category",
                nbins=10,
                title="Distribuição de Preços por Avaliação",
                labels={'price': 'Preço (R$)', 'count': 'Quantidade', 'rating_category': 'Avaliação'},
                color_discrete_sequence=["#8B0000", "#DC143C", "#FF6347", "#FF8C00", "#FFD700"],
                category_orders={"rating_category": [5,4,3,2,1]},
                text_auto=True
            )
            
            fig_price_dist.update_layout(
                title_font_size=22,
                title_x=0.3,
                xaxis=dict(tickformat=","),
                yaxis_title="Quantidade de Livros",
                legend=dict(
                    title="Avaliação (estrelas)",
                    orientation="v",
                    x=1.02,
                    y=1
                )
            )
            
            st.plotly_chart(fig_price_dist, use_container_width=True)

    with col2:
        with st.container(border=True):
            # Top 5 gêneros com melhor custo-benefício (alta avaliação, baixo preço)
            cost_benefit = df_filtered.groupby("genre_desc").agg({
                'rating': 'mean',
                'price': 'mean'
            }).reset_index()
            cost_benefit['cost_benefit_score'] = cost_benefit['rating'] / cost_benefit['price'] * 10
            top_cost_benefit = cost_benefit.nlargest(5, 'cost_benefit_score').sort_values('cost_benefit_score', ascending=True)
            
            fig_cost_benefit = px.bar(
                x=top_cost_benefit['cost_benefit_score'],
                y=top_cost_benefit['genre_desc'],
                title="Top 5 Gêneros - Melhor Custo-Benefício",
                text=top_cost_benefit['cost_benefit_score'].round(1),
                labels={'x': 'Score Custo-Benefício', 'y': 'Gênero'},
                orientation='h',
                color=top_cost_benefit['cost_benefit_score'],
            )
            
            fig_cost_benefit.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_cost_benefit, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <h3>🔍 Insights: Análise Avançada</h3>
    <ul>
    <li><strong>Concentração de Preços:</strong> Livros bem avaliados (4-5 estrelas) se concentram na faixa de R$ 8-15.</li>
    <li><strong>Custo-Benefício Campeão:</strong> Children oferece o melhor custo-benefício, seguido por Romance.</li>
    <li><strong>Estratégia:</strong> Promover gêneros com alto score de custo-benefício para maximizar satisfação e vendas.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
 
    # Footer
    st.markdown("---")

    # Opção para mostrar dados
    with st.expander("📋 Visualizar Dados de Avaliações Filtrados"):
        st.dataframe(df_filtered, use_container_width=True)
        
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "⭐ Dashboard de Análise de Avaliações | Foco na Satisfação do Cliente"
        "</div>", 
        unsafe_allow_html=True
    )