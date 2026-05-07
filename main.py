import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="TechStore Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* Reset y base */
:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1c1c28;
    --accent: #00f5a0;
    --accent2: #00d4ff;
    --danger: #ff4757;
    --warning: #ffa502;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --border: #2a2a3a;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1rem;
}

/* Header */
.store-header {
    background: linear-gradient(135deg, #0a0a0f 0%, #12121a 50%, #0d1a2e 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.store-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,245,160,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.store-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -1px;
}
.store-header p {
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    margin: 0.3rem 0 0;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-card .label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}
.metric-card .value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--accent);
}
.metric-card .sub {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.2rem;
}

/* Product cards */
.product-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.product-card:hover {
    border-color: var(--accent);
}
.product-name {
    font-weight: 700;
    font-size: 1rem;
    color: var(--text);
}
.product-category {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent2);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0.2rem 0;
}
.product-price {
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--accent);
}
.stock-badge {
    display: inline-block;
    padding: 0.1rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
}
.stock-ok { background: rgba(0,245,160,0.15); color: var(--accent); }
.stock-low { background: rgba(255,165,2,0.15); color: var(--warning); }
.stock-out { background: rgba(255,71,87,0.15); color: var(--danger); }

/* Section title */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--text);
    border-left: 3px solid var(--accent);
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem;
    letter-spacing: -0.5px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: #000;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-size: 0.9rem;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    border-radius: 7px;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--accent) !important;
}

/* Dataframe */
.dataframe {
    border-collapse: collapse;
    width: 100%;
}

/* Alerts */
.stSuccess { background: rgba(0,245,160,0.1) !important; border-color: var(--accent) !important; }
.stError { background: rgba(255,71,87,0.1) !important; border-color: var(--danger) !important; }
.stWarning { background: rgba(255,165,2,0.1) !important; border-color: var(--warning) !important; }

/* Hide Streamlit default */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── BASE DE DATOS ─────────────────────────────────────────────────────────────
DB_PATH = "techstore.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            categoria_id INTEGER,
            sku TEXT UNIQUE,
            imagen_emoji TEXT DEFAULT '📦',
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefono TEXT,
            direccion TEXT,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            total REAL NOT NULL,
            estado TEXT DEFAULT 'completada',
            notas TEXT,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS venta_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    # Datos demo
    c.execute("SELECT COUNT(*) FROM categorias")
    if c.fetchone()[0] == 0:
        cats = [
            ("Smartphones", "Teléfonos inteligentes y accesorios"),
            ("Laptops", "Computadoras portátiles"),
            ("Audio", "Audífonos, bocinas y equipos de sonido"),
            ("Gaming", "Consolas, periféricos y accesorios"),
            ("Wearables", "Relojes inteligentes y rastreadores"),
            ("Tablets", "Tablets y e-readers"),
        ]
        c.executemany("INSERT INTO categorias (nombre, descripcion) VALUES (?,?)", cats)

        prods = [
            ("iPhone 16 Pro", "El más avanzado iPhone", 24999.00, 15, 1, "SKU-001", "📱"),
            ("Samsung Galaxy S25", "Flagship Android 2025", 21999.00, 20, 1, "SKU-002", "📱"),
            ("MacBook Pro M4", "Laptop profesional Apple", 49999.00, 8, 2, "SKU-003", "💻"),
            ("Dell XPS 15", "Laptop premium Windows", 35999.00, 12, 2, "SKU-004", "💻"),
            ("AirPods Pro 3", "Audífonos inalámbricos premium", 5999.00, 30, 3, "SKU-005", "🎧"),
            ("Sony WH-1000XM6", "Cancelación de ruido superior", 7499.00, 18, 3, "SKU-006", "🎧"),
            ("PlayStation 5 Pro", "Consola de nueva generación", 17999.00, 5, 4, "SKU-007", "🎮"),
            ("Nintendo Switch 2", "La portátil de Nintendo", 12999.00, 10, 4, "SKU-008", "🎮"),
            ("Apple Watch Ultra 3", "El reloj inteligente más avanzado", 13999.00, 22, 5, "SKU-009", "⌚"),
            ("Samsung Galaxy Tab S10", "Tablet Android premium", 15999.00, 14, 6, "SKU-010", "📟"),
            ("Lenovo ThinkPad X1", "Laptop empresarial robusta", 32999.00, 7, 2, "SKU-011", "💻"),
            ("Xiaomi 15 Ultra", "Flagship con cámara Leica", 18999.00, 25, 1, "SKU-012", "📱"),
            ("JBL Flip 7", "Bocina portátil resistente al agua", 2999.00, 40, 3, "SKU-013", "🔊"),
            ("Corsair K100 RGB", "Teclado mecánico gaming", 4999.00, 16, 4, "SKU-014", "⌨️"),
            ("iPad Air 2025", "La tablet de Apple más versátil", 11999.00, 19, 6, "SKU-015", "📟"),
        ]
        c.executemany(
            "INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id, sku, imagen_emoji) VALUES (?,?,?,?,?,?,?)",
            prods
        )

        clientes = [
            ("Carlos Méndez", "carlos@email.com", "555-1234", "CDMX"),
            ("Ana Rodríguez", "ana@email.com", "555-5678", "Guadalajara"),
            ("Roberto Luna", "roberto@email.com", "555-9012", "Monterrey"),
            ("María Torres", "maria@email.com", "555-3456", "Puebla"),
        ]
        c.executemany(
            "INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (?,?,?,?)",
            clientes
        )

        # Ventas demo
        ventas = [
            (1, 29998.00, "completada", "Entregado"),
            (2, 5999.00, "completada", None),
            (3, 49999.00, "pendiente", "Esperando pago"),
            (4, 17999.00, "completada", None),
        ]
        c.executemany(
            "INSERT INTO ventas (cliente_id, total, estado, notas) VALUES (?,?,?,?)",
            ventas
        )
        items = [
            (1, 1, 1, 24999.00), (1, 5, 1, 5999.00),
            (2, 5, 1, 5999.00),
            (3, 3, 1, 49999.00),
            (4, 7, 1, 17999.00),
        ]
        c.executemany(
            "INSERT INTO venta_items (venta_id, producto_id, cantidad, precio_unitario) VALUES (?,?,?,?)",
            items
        )

    conn.commit()
    conn.close()

# ─── QUERIES ──────────────────────────────────────────────────────────────────
def get_productos(categoria_id=None, busqueda=""):
    conn = get_conn()
    q = """
        SELECT p.*, c.nombre as categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE 1=1
    """
    params = []
    if categoria_id:
        q += " AND p.categoria_id = ?"
        params.append(categoria_id)
    if busqueda:
        q += " AND (p.nombre LIKE ? OR p.descripcion LIKE ? OR p.sku LIKE ?)"
        b = f"%{busqueda}%"
        params.extend([b, b, b])
    q += " ORDER BY p.nombre"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df

def get_categorias():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM categorias ORDER BY nombre", conn)
    conn.close()
    return df

def get_clientes():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM clientes ORDER BY nombre", conn)
    conn.close()
    return df

def get_ventas():
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT v.*, cl.nombre as cliente_nombre
        FROM ventas v
        LEFT JOIN clientes cl ON v.cliente_id = cl.id
        ORDER BY v.creado_en DESC
    """, conn)
    conn.close()
    return df

def get_metricas():
    conn = get_conn()
    c = conn.cursor()
    total_ventas = c.execute("SELECT COALESCE(SUM(total),0) FROM ventas WHERE estado='completada'").fetchone()[0]
    num_ventas = c.execute("SELECT COUNT(*) FROM ventas").fetchone()[0]
    total_productos = c.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    total_clientes = c.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    conn.close()
    return total_ventas, num_ventas, total_productos, total_clientes

def agregar_producto(nombre, desc, precio, stock, cat_id, sku, emoji):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id, sku, imagen_emoji) VALUES (?,?,?,?,?,?,?)",
            (nombre, desc, precio, stock, cat_id, sku, emoji)
        )
        conn.commit()
        return True, "Producto agregado exitosamente ✓"
    except sqlite3.IntegrityError:
        return False, "SKU ya existe. Usa uno diferente."
    finally:
        conn.close()

def actualizar_stock(producto_id, nuevo_stock):
    conn = get_conn()
    conn.execute("UPDATE productos SET stock=? WHERE id=?", (nuevo_stock, producto_id))
    conn.commit()
    conn.close()

def eliminar_producto(producto_id):
    conn = get_conn()
    conn.execute("DELETE FROM productos WHERE id=?", (producto_id,))
    conn.commit()
    conn.close()

def agregar_cliente(nombre, email, tel, dir):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (?,?,?,?)",
            (nombre, email, tel, dir)
        )
        conn.commit()
        return True, "Cliente registrado ✓"
    except sqlite3.IntegrityError:
        return False, "Email ya registrado."
    finally:
        conn.close()

def registrar_venta(cliente_id, items_venta):
    conn = get_conn()
    try:
        total = sum(p * q for _, p, q in items_venta)
        cur = conn.execute(
            "INSERT INTO ventas (cliente_id, total, estado) VALUES (?,?,'completada')",
            (cliente_id, total)
        )
        venta_id = cur.lastrowid
        for prod_id, precio, cant in items_venta:
            conn.execute(
                "INSERT INTO venta_items (venta_id, producto_id, cantidad, precio_unitario) VALUES (?,?,?,?)",
                (venta_id, prod_id, cant, precio)
            )
            conn.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (cant, prod_id)
            )
        conn.commit()
        return True, f"Venta #{venta_id} registrada — Total: ${total:,.2f}"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def agregar_categoria(nombre, desc):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?,?)", (nombre, desc))
        conn.commit()
        return True, "Categoría creada ✓"
    except sqlite3.IntegrityError:
        return False, "Categoría ya existe."
    finally:
        conn.close()

# ─── INIT ─────────────────────────────────────────────────────────────────────
init_db()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ TechStore Pro")
    st.markdown("---")
    pagina = st.radio(
        "Navegación",
        ["🏠 Dashboard", "📦 Productos", "🛒 Nueva Venta", "📋 Ventas", "👥 Clientes", "🗂️ Categorías"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        "<div style='font-family:Space Mono,monospace;font-size:0.7rem;color:#6b6b80;'>TechStore Pro v2.0<br>Base de datos: SQLite</div>",
        unsafe_allow_html=True
    )

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="store-header">
    <h1>⚡ TechStore Pro</h1>
    <p>Sistema de gestión de tienda electrónica</p>
</div>
""", unsafe_allow_html=True)

# ─── PÁGINAS ──────────────────────────────────────────────────────────────────

# ── DASHBOARD ──────────────────────────────────────────────────────────────────
if pagina == "🏠 Dashboard":
    total_v, num_v, total_p, total_c = get_metricas()

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="label">💰 Ingresos Totales</div>
            <div class="value">${total_v:,.0f}</div>
            <div class="sub">Ventas completadas</div>
        </div>
        <div class="metric-card">
            <div class="label">🛒 Total Ventas</div>
            <div class="value">{num_v}</div>
            <div class="sub">Órdenes registradas</div>
        </div>
        <div class="metric-card">
            <div class="label">📦 Productos</div>
            <div class="value">{total_p}</div>
            <div class="sub">En catálogo</div>
        </div>
        <div class="metric-card">
            <div class="label">👥 Clientes</div>
            <div class="value">{total_c}</div>
            <div class="sub">Registrados</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-title">Ventas Recientes</div>', unsafe_allow_html=True)
        ventas = get_ventas().head(6)
        if not ventas.empty:
            for _, v in ventas.iterrows():
                estado_color = "#00f5a0" if v["estado"] == "completada" else "#ffa502"
                st.markdown(f"""
                <div class="product-card" style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div class="product-name">Venta #{v['id']} — {v['cliente_nombre'] or 'S/C'}</div>
                        <div class="product-category">{v['creado_en'][:16]}</div>
                    </div>
                    <div style="text-align:right">
                        <div class="product-price">${v['total']:,.2f}</div>
                        <span style="color:{estado_color};font-size:0.75rem;font-family:'Space Mono',monospace;">{v['estado'].upper()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Stock Crítico</div>', unsafe_allow_html=True)
        prods = get_productos()
        criticos = prods[prods["stock"] <= 8].sort_values("stock").head(6)
        for _, p in criticos.iterrows():
            badge = "stock-out" if p["stock"] == 0 else "stock-low"
            label = "AGOTADO" if p["stock"] == 0 else f"{p['stock']} uds"
            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{p['imagen_emoji']}</span>
                        <span class="product-name"> {p['nombre'][:25]}</span>
                    </div>
                    <span class="stock-badge {badge}">{label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Resumen por Categoría</div>', unsafe_allow_html=True)
    conn = get_conn()
    cat_stats = pd.read_sql_query("""
        SELECT c.nombre, COUNT(p.id) as productos, SUM(p.stock) as stock_total,
               AVG(p.precio) as precio_promedio
        FROM categorias c
        LEFT JOIN productos p ON p.categoria_id = c.id
        GROUP BY c.id, c.nombre
    """, conn)
    conn.close()
    cat_stats["precio_promedio"] = cat_stats["precio_promedio"].apply(lambda x: f"${x:,.0f}" if x else "$0")
    st.dataframe(cat_stats, use_container_width=True, hide_index=True)

# ── PRODUCTOS ─────────────────────────────────────────────────────────────────
elif pagina == "📦 Productos":
    tab1, tab2 = st.tabs(["📋 Catálogo", "➕ Agregar Producto"])

    with tab1:
        col_b, col_c, col_s = st.columns([2, 2, 1])
        with col_b:
            busqueda = st.text_input("🔍 Buscar producto...", placeholder="Nombre, SKU, descripción...")
        with col_c:
            cats = get_categorias()
            cat_opts = {"Todas": None} | dict(zip(cats["nombre"], cats["id"]))
            cat_sel = st.selectbox("Categoría", list(cat_opts.keys()))
        with col_s:
            orden = st.selectbox("Ordenar por", ["Nombre", "Precio ↑", "Precio ↓", "Stock"])

        prods = get_productos(cat_opts[cat_sel], busqueda)

        if orden == "Precio ↑":
            prods = prods.sort_values("precio")
        elif orden == "Precio ↓":
            prods = prods.sort_values("precio", ascending=False)
        elif orden == "Stock":
            prods = prods.sort_values("stock")

        st.markdown(f"<div style='color:var(--muted);font-size:0.8rem;margin-bottom:1rem;'>{len(prods)} productos encontrados</div>", unsafe_allow_html=True)

        cols = st.columns(3)
        for i, (_, p) in enumerate(prods.iterrows()):
            badge = "stock-ok" if p["stock"] > 10 else ("stock-low" if p["stock"] > 0 else "stock-out")
            label = f"{p['stock']} uds" if p["stock"] > 0 else "AGOTADO"
            with cols[i % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">{p['imagen_emoji']}</div>
                    <div class="product-name">{p['nombre']}</div>
                    <div class="product-category">{p['categoria_nombre'] or '—'} · {p['sku']}</div>
                    <div class="product-price">${p['precio']:,.2f}</div>
                    <div style="margin-top:0.5rem;display:flex;justify-content:space-between;align-items:center;">
                        <span class="stock-badge {badge}">{label}</span>
                        <span style="font-size:0.7rem;color:var(--muted);">ID: {p['id']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("Gestionar"):
                    nuevo_stock = st.number_input(
                        "Nuevo stock", min_value=0, value=int(p["stock"]),
                        key=f"stock_{p['id']}"
                    )
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Actualizar", key=f"upd_{p['id']}"):
                            actualizar_stock(p["id"], nuevo_stock)
                            st.success("Stock actualizado")
                            st.rerun()
                    with c2:
                        if st.button("🗑️ Eliminar", key=f"del_{p['id']}"):
                            eliminar_producto(p["id"])
                            st.success("Eliminado")
                            st.rerun()

    with tab2:
        st.markdown('<div class="section-title">Nuevo Producto</div>', unsafe_allow_html=True)
        cats = get_categorias()
        emojis = ["📱", "💻", "🎧", "🎮", "⌚", "📟", "🔊", "⌨️", "🖥️", "📷", "🎙️", "📦"]

        with st.form("form_producto"):
            c1, c2 = st.columns(2)
            with c1:
                np_nombre = st.text_input("Nombre del producto *")
                np_precio = st.number_input("Precio (MXN) *", min_value=0.01, step=1.0)
                np_sku = st.text_input("SKU *", placeholder="SKU-XXX")
            with c2:
                np_cat = st.selectbox("Categoría *", cats["nombre"].tolist())
                np_stock = st.number_input("Stock inicial", min_value=0, value=0)
                np_emoji = st.selectbox("Icono", emojis)
            np_desc = st.text_area("Descripción", height=80)
            submitted = st.form_submit_button("➕ Agregar Producto", use_container_width=True)
            if submitted:
                if not np_nombre or not np_sku:
                    st.error("Nombre y SKU son obligatorios.")
                else:
                    cat_id = int(cats[cats["nombre"] == np_cat]["id"].values[0])
                    ok, msg = agregar_producto(np_nombre, np_desc, np_precio, np_stock, cat_id, np_sku, np_emoji)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

# ── NUEVA VENTA ────────────────────────────────────────────────────────────────
elif pagina == "🛒 Nueva Venta":
    st.markdown('<div class="section-title">Registrar Nueva Venta</div>', unsafe_allow_html=True)

    if "carrito" not in st.session_state:
        st.session_state.carrito = []

    clientes = get_clientes()
    prods = get_productos()
    prods_disp = prods[prods["stock"] > 0]

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("**Cliente**")
        cliente_opts = dict(zip(clientes["nombre"] + " (" + clientes["email"] + ")", clientes["id"]))
        cliente_sel = st.selectbox("Seleccionar cliente", list(cliente_opts.keys()))

        st.markdown("**Agregar producto al carrito**")
        prod_opts = dict(zip(
            prods_disp["imagen_emoji"] + " " + prods_disp["nombre"] + f" (${0})" if False else
            [f"{r['imagen_emoji']} {r['nombre']} — ${r['precio']:,.2f}" for _, r in prods_disp.iterrows()],
            prods_disp["id"].tolist()
        ))
        if prod_opts:
            prod_sel = st.selectbox("Producto", list(prod_opts.keys()))
            prod_id = prod_opts[prod_sel]
            prod_info = prods_disp[prods_disp["id"] == prod_id].iloc[0]
            cantidad = st.number_input(
                f"Cantidad (máx. {prod_info['stock']})",
                min_value=1, max_value=int(prod_info["stock"]), value=1
            )
            if st.button("🛒 Agregar al carrito"):
                # Verificar si ya está en carrito
                existe = False
                for item in st.session_state.carrito:
                    if item["id"] == prod_id:
                        item["cantidad"] += cantidad
                        existe = True
                        break
                if not existe:
                    st.session_state.carrito.append({
                        "id": prod_id,
                        "nombre": prod_info["nombre"],
                        "precio": prod_info["precio"],
                        "cantidad": cantidad,
                        "emoji": prod_info["imagen_emoji"],
                    })
                st.success(f"{prod_info['imagen_emoji']} Agregado al carrito")
                st.rerun()
        else:
            st.warning("No hay productos con stock disponible.")

    with col2:
        st.markdown("**🛒 Carrito**")
        if not st.session_state.carrito:
            st.info("El carrito está vacío.")
        else:
            total = 0
            for i, item in enumerate(st.session_state.carrito):
                subtotal = item["precio"] * item["cantidad"]
                total += subtotal
                st.markdown(f"""
                <div class="product-card">
                    <div style="display:flex;justify-content:space-between;">
                        <div>
                            <span>{item['emoji']}</span>
                            <strong>{item['nombre'][:20]}</strong><br>
                            <span style="font-size:0.75rem;color:var(--muted);">{item['cantidad']} × ${item['precio']:,.2f}</span>
                        </div>
                        <div style="color:var(--accent);font-weight:700;">${subtotal:,.2f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"✕ Quitar", key=f"quitar_{i}"):
                    st.session_state.carrito.pop(i)
                    st.rerun()

            st.markdown(f"""
            <div style="background:var(--surface2);border-radius:10px;padding:1rem;margin-top:1rem;border:1px solid var(--accent);">
                <div style="display:flex;justify-content:space-between;font-size:1.3rem;font-weight:800;">
                    <span>TOTAL</span>
                    <span style="color:var(--accent);">${total:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✅ Confirmar Venta", use_container_width=True):
                cliente_id = cliente_opts[cliente_sel]
                items_venta = [(i["id"], i["precio"], i["cantidad"]) for i in st.session_state.carrito]
                ok, msg = registrar_venta(cliente_id, items_venta)
                if ok:
                    st.success(msg)
                    st.session_state.carrito = []
                    st.rerun()
                else:
                    st.error(msg)

            if st.button("🗑️ Vaciar carrito"):
                st.session_state.carrito = []
                st.rerun()

# ── VENTAS ────────────────────────────────────────────────────────────────────
elif pagina == "📋 Ventas":
    st.markdown('<div class="section-title">Historial de Ventas</div>', unsafe_allow_html=True)
    ventas = get_ventas()

    col1, col2, col3 = st.columns(3)
    with col1:
        total = ventas["total"].sum()
        st.metric("💰 Total Ingresos", f"${total:,.2f}")
    with col2:
        completadas = ventas[ventas["estado"] == "completada"]["total"].sum()
        st.metric("✅ Completadas", f"${completadas:,.2f}")
    with col3:
        pendientes = ventas[ventas["estado"] == "pendiente"]["total"].sum()
        st.metric("⏳ Pendientes", f"${pendientes:,.2f}")

    st.markdown("---")

    if not ventas.empty:
        for _, v in ventas.iterrows():
            estado_color = "#00f5a0" if v["estado"] == "completada" else "#ffa502"
            st.markdown(f"""
            <div class="product-card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div class="product-name">Venta #{v['id']}</div>
                    <div class="product-category">Cliente: {v['cliente_nombre'] or 'Sin cliente'}</div>
                    <div style="font-size:0.75rem;color:var(--muted);">{v['creado_en'][:16]}</div>
                </div>
                <div style="text-align:right;">
                    <div class="product-price">${v['total']:,.2f}</div>
                    <span style="color:{estado_color};font-family:'Space Mono',monospace;font-size:0.75rem;">● {v['estado'].upper()}</span>
                    {f'<div style="font-size:0.7rem;color:var(--muted);">{v["notas"]}</div>' if v["notas"] else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Exportar datos**")
        csv = ventas.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "ventas.csv", "text/csv")

# ── CLIENTES ──────────────────────────────────────────────────────────────────
elif pagina == "👥 Clientes":
    tab1, tab2 = st.tabs(["📋 Clientes", "➕ Nuevo Cliente"])

    with tab1:
        clientes = get_clientes()
        st.markdown(f"<div style='color:var(--muted);font-size:0.8rem;margin-bottom:1rem;'>{len(clientes)} clientes registrados</div>", unsafe_allow_html=True)
        for _, cl in clientes.iterrows():
            st.markdown(f"""
            <div class="product-card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div class="product-name">👤 {cl['nombre']}</div>
                    <div class="product-category">{cl['email']}</div>
                    <div style="font-size:0.75rem;color:var(--muted);">📞 {cl['telefono'] or '—'}  📍 {cl['direccion'] or '—'}</div>
                </div>
                <div style="text-align:right;">
                    <div style="color:var(--muted);font-size:0.75rem;font-family:'Space Mono',monospace;">ID #{cl['id']}</div>
                    <div style="font-size:0.7rem;color:var(--muted);">Desde {cl['creado_en'][:10]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-title">Registrar Cliente</div>', unsafe_allow_html=True)
        with st.form("form_cliente"):
            c1, c2 = st.columns(2)
            with c1:
                nc_nombre = st.text_input("Nombre completo *")
                nc_tel = st.text_input("Teléfono")
            with c2:
                nc_email = st.text_input("Email *")
                nc_dir = st.text_input("Dirección / Ciudad")
            submitted = st.form_submit_button("👥 Registrar Cliente", use_container_width=True)
            if submitted:
                if not nc_nombre or not nc_email:
                    st.error("Nombre y email son obligatorios.")
                else:
                    ok, msg = agregar_cliente(nc_nombre, nc_email, nc_tel, nc_dir)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

# ── CATEGORÍAS ────────────────────────────────────────────────────────────────
elif pagina == "🗂️ Categorías":
    tab1, tab2 = st.tabs(["📋 Categorías", "➕ Nueva Categoría"])

    with tab1:
        cats = get_categorias()
        for _, cat in cats.iterrows():
            n_prods = len(get_productos(cat["id"]))
            st.markdown(f"""
            <div class="product-card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div class="product-name">🗂️ {cat['nombre']}</div>
                    <div style="font-size:0.8rem;color:var(--muted);">{cat['descripcion'] or 'Sin descripción'}</div>
                </div>
                <div style="text-align:right;">
                    <span class="stock-badge stock-ok">{n_prods} productos</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-title">Nueva Categoría</div>', unsafe_allow_html=True)
        with st.form("form_cat"):
            nc_nombre = st.text_input("Nombre de la categoría *")
            nc_desc = st.text_area("Descripción", height=80)
            submitted = st.form_submit_button("🗂️ Crear Categoría", use_container_width=True)
            if submitted:
                if not nc_nombre:
                    st.error("El nombre es obligatorio.")
                else:
                    ok, msg = agregar_categoria(nc_nombre, nc_desc)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)