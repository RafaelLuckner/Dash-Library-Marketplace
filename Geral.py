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
st.markdown('<h1 class="main-header">📊 Dashboard de Vendas - Análise de Mercado</h1>', unsafe_allow_html=True)


def plot_bar_chart(data, x_col, y_col, title, x_label, y_label):
    fig = px.bar(
        x=data[x_col],
        y=data[y_col],
        title= title,
        text= data[x_col].values.round(0).astype(int),
        labels={'x': x_label, 'y': y_label},
        orientation='h',
        color=data[x_col],
    )

    fig.update_layout(
        title_font_size=22,
        title_x=0.3,
        coloraxis_showscale=False  
    )


    st.plotly_chart(fig, use_container_width=True)


df = load_data()
# Métricas gerais
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📚 Total de Vendas", f"{len(df):,}", border=True)
with col2:
    st.metric("💰 Receita Total", f"R$ {df['price'].sum():,.2f}", border=True)
with col3:
    st.metric("📈 Preço Médio por", f"R$ {df['price'].mean():.2f}", border=True)
with col4:
    st.metric("🎯 Gêneros Ativos", len(df['genre_desc'].unique()), border=True)


df_filtered = filter_data()

if df_filtered.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados. Tente ajustar os filtros.")
else:

    # Gráficos principais
    st.markdown("## 📈 Análise por Gênero Literário")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border = True):

            # Gráfico de preço médio por gênero (Plotly)
            avg_price_genre = df_filtered.groupby("genre_desc")["price"].mean().sort_values(ascending=True)
            
            fig_price = px.bar(
                x=avg_price_genre.values,
                y=avg_price_genre.index,
                title="Preço Médio por Gênero",
                text= avg_price_genre.values.round(2),
                labels={'x': 'Preço Médio (R$)', 'y': 'Gênero'},
                color=avg_price_genre.values,
                orientation='h',
            )

            fig_price.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False  
            )


            st.plotly_chart(fig_price, use_container_width=True)

    with col2:
        with st.container(border = True):
            # Gráfico de vendas por gênero (Plotly)
            sales_count = df_filtered["genre_desc"].value_counts().sort_values(ascending=True)
            
            fig_sales = px.bar(
                x=sales_count.values,
                y=sales_count.index,
                title="Número de Vendas por Gênero",
                text= sales_count.values,
                labels={'x': 'Número de Vendas', 'y': 'Gênero'},
                color=sales_count.values,
                orientation='h',

            )
            fig_sales.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False  
            )
            
            st.plotly_chart(fig_sales, use_container_width=True)

    # Insights sobre gêneros
    st.markdown("""
    <div class="insight-box">
    <h3>🎯 Insights: Gênero Literário</h3>
    <ul>
    <li><strong>Sci-Fi/Fantasy</strong> domina como o gênero mais vendido, seguido de Mystery e Romance.</li>
    <li><strong>Estratégia:</strong> Priorizar promoções, eventos e novos lançamentos nesses gêneros para maximizar vendas.</li>
    <li><strong>Oportunidade:</strong> Gêneros como Memoir e Nonfiction têm preços mais elevados porém baixa quantidade de vendas, podendo ser uma área a ser explorada com campanhas direcionadas.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Análise temporal
    st.markdown("## 📅 Análise Temporal de Vendas")

    # Preparar dados temporais
    df_filtered["sale_date"] = pd.to_datetime(df_filtered["sale_date"])
    df_filtered["month"] = df_filtered["sale_date"].dt.month_name()
    df_filtered["total_discount"] = df_filtered["price"] * df_filtered["discount"]

    month_order = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border = True):
            # Vendas por mês
            sales_per_month = df_filtered.groupby("month")["price"].sum().reindex(month_order).fillna(0)

            # Cria os textos somente para os 3 maiores valores
            top_3_months = sales_per_month.nlargest(3)
            bottom_3_months = sales_per_month.nsmallest(3)

            text_labels = [int(val) if month in top_3_months.index or month in bottom_3_months.index else None for month, val in sales_per_month.items()]

            # Cria o gráfico
            fig_monthly_sales = px.line(
                x=sales_per_month.index,
                y=sales_per_month.values,
                title="Evolução das Vendas Mensais",
                labels={'x': 'Mês', 'y': 'Valor Total de Vendas (R$)'},
                text=text_labels,
                markers=True
            )

            fig_monthly_sales.update_traces(
                line=dict(color='#2E86AB', width=3),
                marker=dict(size=8, color="#060079"),
                textposition="top center",
                textfont=dict(size=13)
            )

            fig_monthly_sales.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False,
            )

            st.plotly_chart(fig_monthly_sales, use_container_width=True)

    with col2:
        with st.container(border = True):

            # Descontos por mês
            discounts_per_month = df_filtered.groupby("month")["total_discount"].sum().reindex(month_order).fillna(0)
            
            fig_discounts = px.bar(
                x=discounts_per_month.index,
                y=discounts_per_month.values,
                title="Valor Total de Descontos por Mês",
                labels={'x': 'Mês', 'y': 'Valor Total de Descontos (R$)'},
                text=  discounts_per_month.values.round(0).astype(int),
                color=discounts_per_month.values,
                color_continuous_scale="reds",
                
            )
            fig_discounts.update_layout(
                title_font_size=22,
                title_x=0.3,
                coloraxis_showscale=False  
            )
            

            st.plotly_chart(fig_discounts, use_container_width=True)

    # Insight temporal
    st.markdown("""
    <div class="insight-box">
    <h3>📊 Insights: Sazonalidade</h3>
    <ul>
    <li><strong>Dezembro</strong> apresenta o maior valor de descontos, apesar de não ser o mês com mais vendas, sendo Agosto e Julho </li>
    <li><strong>Estratégia:</strong> Priorizar os meses de Agosto e Julho por conta de maior quantidade de vendas com menor valor de desconto.</li>
    <li><strong>Oportunidade:</strong> Preparar ações específicas para meses com menor engajamento como Janeiro e Fevereiro.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Análise de correlação
    st.markdown("## 🔍 Análise Avançada")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border = True):

            fig_dist = px.histogram(
                df_filtered,
                x="price",
                nbins=10,
                title="Distribuição de Vendas por Preços",
                labels={'price': 'Preço (R$)'},
                color_discrete_sequence=["#1a3293"],
                text_auto=True
            )

            fig_dist.update_layout(
                title_font_size=22,
                xaxis=dict(
                    tickformat=",",
                ),
                yaxis_title="Quantidade de Vendas",
                margin=dict(t=60, l=40, r=40, b=40),
                title_x=0.3
            )

            fig_dist.update_traces(marker_line_width=1, marker_line_color="#ffffff")

            st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        with st.container(border = True):

            # Top 10 gêneros por receita
            revenue_by_genre = df_filtered.groupby("genre_desc")["price"].sum().sort_values(ascending=True).tail(5)
            
            plot_bar_chart(
                data=revenue_by_genre.reset_index(),
                x_col="price",
                y_col="genre_desc",
                title="Top 5 Gêneros por Receita",
                x_label="Receita (R$)",
                y_label="Gênero"
            )
    st.markdown("""
            <div class="insight-box">
            <h3>📊 Insights: Preços e Receita por Gênero</h3>
            <ul>
            <li><strong>Concentração de Vendas:</strong> A maior parte das vendas ocorre em faixas de preço abaixo de R$ 15, com pico em torno de R$ 10.</li>
            <li><strong>Receita por Gênero:</strong> Apesar da concentração em preços baixos, o gênero <strong>SciFi/Fantasy</strong> gera a maior receita, mais que o dobro do segundo colocado (<strong>Mystery</strong>).</li>
            <li><strong>Oportunidade:</strong> Promover livros de alta receita, como os de <strong>SciFi/Fantasy</strong>, mesmo com preços acessíveis, pode ser uma estratégia eficiente para maximizar lucro.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")

    # Opção para mostrar dados
    with st.expander("📋 Visualizar Dados Filtrados"):
        st.dataframe(df_filtered, use_container_width=True)
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "📚 Dashboard de Análise de Vendas - Livraria | Desenvolvido com Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )