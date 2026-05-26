import streamlit as st
from babel.numbers import format_decimal, format_currency

from configurations import MONGO_DB_REAL_ESTATE_TABLE, CONTACT_NUMBER
from mongodb_manager import MongoDBManager

# Page Tab Title & Layout
st.set_page_config(page_title="Dhammi Enterprises", layout="wide")

# Page Style CSS
css = """
<style>
    [data-testid="stHeader"]{
        display: none;
    }
    
    .h_1 {
        font-size: 16px;
    }
    .h_1_value {
        font-size: 14px;
        font-weight: bold;
    }
    .container {
      display: Inline-flex;             
      gap: 10px;               /* space between divs */
      justify-content: left;
      align-items: center;
      # flex-wrap: wrap;        /* responsive on small screens */
      margin-left:5%;
      margin-bottom:10px;
    }
    .box {
      float:left;
      padding: 30px;
      background: #FBCC131A;
      border-radius: 12px;
      text-align: center;
      font-size: 12px;
      font-family: Arial, sans-serif;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      box-sizing: border-box;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

if __name__ == "__main__":
    # Header Section
    st.markdown(
        """
        <div style='text-align:center; padding-top:20px;'>
            <h1 style='font-size:48px; margin-bottom:0;'>Dhammi Enterprises</h1>
            <p style='font-size:22px; color:gray;'>Real Estate Catalogue</p>
        </div>
        """, unsafe_allow_html=True)
    # Get All Real Estates
    st.markdown("---")
    mongo = MongoDBManager()
    with st.spinner("Loading Data..."):
        properties = mongo.getAllData(MONGO_DB_REAL_ESTATE_TABLE)

    # Property Listings
    for property in properties:
        col1, col2 = st.columns([1, 2])
        with col1:
            try:
                st.image(property["image"])
            except:
                st.image("https://dummyimage.com/600x400.png")
        with col2:
            property_content = f"""
                <div style="display: flex;">
                    <div class=container>
                        <div style='font-weight:bold; font-size:28px;'>📍{property['location']}</div>
                        <div> ↗ {property['direction']}</div>
                    </div>
                        <div style="margin-left:auto;">Ph. +91 {CONTACT_NUMBER}</div>
                </div>
                
                <div class=container>
                    <div class=box style='min-width:20%'>
                       <div class=h_1 >🏷 Price<br> </div>
                        <div class=h_1_value>{format_currency(property['price_per_gaz'], 'INR', '#,##,##0', locale='en_IN', currency_digits=False)}/Sq Yd </div>
                    </div>
                    <div class=box>
                        <div class=h_1> ⎕ Area<br> </div>
                        <div class=h_1_value>{format_decimal(property['area_size_in_gaz'], locale='en_IN')} Sq Yd </div>
                    </div>
                    <div class=box>
                        <div class=h_1>🟰 Total Costing<br></div>
                        <div class=h_1_value>{format_currency(property['price_per_gaz'] * property['area_size_in_gaz'], 'INR', '#,##,##0', locale='en_IN', currency_digits=False)}</div>
                    </div>
                </div>
                
                <div class=container style='gap:0px;'>
                    <div class=box style='background: rgb(255,255,255);font-size:30px;box-shadow:none;'>🏠</div> 
                    <div class=box style='background: rgb(255,255,255);font-size:16px;box-shadow:none;'>Description</div> 
                    <div class=box style='background: rgb(255,255,255);font-size:14px;box-shadow:none;'>{property["description"]}</div>
                </div>
                
                <div style="width: 100%;background: linear-gradient(135deg, #22c55e, #16a34a);color: white;padding: 2px;border-radius: 14px;text-align: center;box-shadow: 0 4px 12px rgba(34, 197, 94, 0.25);">For Sale</div>
            
            """
            st.markdown(property_content, unsafe_allow_html=True)
        st.markdown("---")

    # Footer
    st.markdown(
        f"""
        <div style='text-align:center; color:gray; padding:20px;'>
            © 2026 Dhammi Enterprises | Real Estate Listings<br>
            Contact: +91-{CONTACT_NUMBER}
        </div>
        """, unsafe_allow_html=True)
