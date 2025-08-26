import streamlit as st
import random
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="🔋 Battery Cell Monitor",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for simple styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    
    .cell-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    .status-good { color: #28a745; font-weight: bold; }
    .status-warning { color: #ffc107; font-weight: bold; }
    .status-danger { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'list_of_cell' not in st.session_state:
    st.session_state.list_of_cell = []
if 'cell_no' not in st.session_state:
    st.session_state.cell_no = 0

def get_cell_status(voltage, min_voltage, max_voltage, temp):
    """Determine cell status based on parameters"""
    voltage_ok = min_voltage <= voltage <= max_voltage
    temp_ok = 25 <= temp <= 40
    
    if voltage_ok and temp_ok:
        return "🟢 Good", "status-good"
    elif not voltage_ok:
        return "🔴 Critical", "status-danger"
    else:
        return "🟡 Warning", "status-warning"

# Main header
st.markdown('<h1 class="main-header">🔋 Battery Cell Monitor</h1>', unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Cell Setup")
    
    # Step 1: Number of cells (from your original code)
    cell_no = st.number_input("Enter the number of cells:", min_value=1, max_value=20, value=1, step=1)
    
    if st.button("Initialize Cells"):
        st.session_state.cell_no = cell_no
        st.session_state.list_of_cell = []
        st.session_state.cells_data = {}
    
    # Step 2: Cell type selection (from your original code)
    if st.session_state.cell_no > 0:
        st.subheader("Enter Cell Types")
        
        for i in range(st.session_state.cell_no):
            cell_type = st.selectbox(
                f"Cell {i+1} type:", 
                ["lfp", "nmc"], 
                key=f"cell_type_{i}"
            )
            
            if len(st.session_state.list_of_cell) <= i:
                st.session_state.list_of_cell.append(cell_type)
            else:
                st.session_state.list_of_cell[i] = cell_type
        
        if st.button("Create Cell Data"):
            # Your original cell data creation logic
            st.session_state.cells_data = {}
            
            for idx, cell_type in enumerate(st.session_state.list_of_cell, start=1):
                cell_key = f"cell_{idx}_{cell_type}"
                
                # Your original voltage logic
                voltage = 3.2 if cell_type == "lfp" else 3.6
                min_voltage = 2.8 if cell_type == "lfp" else 3.2
                max_voltage = 3.6 if cell_type == "lfp" else 4.0
                current = 0.0
                temp = round(random.uniform(25, 40), 1)  # Your original temp logic
                capacity = round(voltage * current, 2)  # Your original capacity logic

                st.session_state.cells_data[cell_key] = {
                    "voltage": voltage,
                    "current": current,
                    "temp": temp,
                    "capacity": capacity,
                    "min_voltage": min_voltage,
                    "max_voltage": max_voltage
                }
    
    # Step 3: Current input (from your original code)
    if st.session_state.cells_data:
        st.subheader("Enter Current Values")
        
        for key in st.session_state.cells_data:
            try:
                current = st.number_input(
                    f"Current for {key} (A):", 
                    value=st.session_state.cells_data[key]["current"],
                    step=0.1,
                    key=f"current_input_{key}"
                )
                
                # Your original capacity update logic
                voltage = st.session_state.cells_data[key]["voltage"]
                st.session_state.cells_data[key]["current"] = current
                st.session_state.cells_data[key]["capacity"] = round(voltage * current, 2)
                
            except ValueError:
                st.error("Invalid input. Setting current to 0.")
                st.session_state.cells_data[key]["current"] = 0.0

with col2:
    if st.session_state.cells_data:
        st.header("Cell Data Display")
        
        # Overview metrics
        total_cells = len(st.session_state.cells_data)
        avg_voltage = sum(cell["voltage"] for cell in st.session_state.cells_data.values()) / total_cells
        avg_temp = sum(cell["temp"] for cell in st.session_state.cells_data.values()) / total_cells
        total_capacity = sum(cell["capacity"] for cell in st.session_state.cells_data.values())
        
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.metric("Total Cells", total_cells)
        with col_b:
            st.metric("Avg Voltage", f"{avg_voltage:.2f}V")
        with col_c:
            st.metric("Avg Temp", f"{avg_temp:.1f}°C")
        with col_d:
            st.metric("Total Capacity", f"{total_capacity:.2f}Wh")
        
        st.divider()
        
        # Individual cell display (similar to your original print output)
        st.subheader("Updated Cell Data")
        
        for key, values in st.session_state.cells_data.items():
            status, status_class = get_cell_status(
                values["voltage"], 
                values["min_voltage"], 
                values["max_voltage"],
                values["temp"]
            )
            
            with st.container():
                st.markdown(f'<div class="cell-card">', unsafe_allow_html=True)
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.write(f"**{key}:**")
                    st.write(f"• Voltage: {values['voltage']}V")
                    st.write(f"• Current: {values['current']}A")
                    st.write(f"• Temperature: {values['temp']}°C")
                
                with col_right:
                    st.write(f"**Status:** {status}")
                    st.write(f"• Capacity: {values['capacity']}Wh")
                    st.write(f"• Range: {values['min_voltage']}V - {values['max_voltage']}V")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Data table (replicating your original dictionary output)
        st.subheader("Raw Data (Dictionary Format)")
        
        # Display in the format similar to your original print statement
        for key, values in st.session_state.cells_data.items():
            st.code(f"{key}: {values}")
        
        # DataFrame version
        st.subheader("Table View")
        df_data = []
        for key, cell_data in st.session_state.cells_data.items():
            df_data.append({
                "Cell ID": key,
                "Voltage (V)": cell_data["voltage"],
                "Current (A)": cell_data["current"],
                "Temperature (°C)": cell_data["temp"],
                "Capacity (Wh)": cell_data["capacity"],
                "Min Voltage (V)": cell_data["min_voltage"],
                "Max Voltage (V)": cell_data["max_voltage"]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="battery_cell_data.csv",
            mime="text/csv"
        )

    else:
        st.info("👈 Please set up your cells using the controls on the left!")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Based on your original battery cell monitoring code")