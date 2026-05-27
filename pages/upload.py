import time
import uuid
from datetime import datetime

import streamlit as st
import streamlit_authenticator as stauth
from babel.numbers import format_decimal, format_currency
from bson.binary import Binary
from configurations import MONGO_DB_REAL_ESTATE_TABLE, MONGO_DB_USER, CONTACT_NUMBER
from mongodb_manager import MongoDBManager
from streamlit_geolocation import streamlit_geolocation

mongo = MongoDBManager()

data = mongo.getAllData(table=MONGO_DB_USER)
data = {row["username"]: {"name": row["name"], "password": row["password"]} for row in data}
cred = {"usernames": data}
authenticator = stauth.Authenticate(credentials=cred, cookie_name="update_dashboard", cookie_key="update_key",
                                    cookie_expiry_days=10)
authenticator.login(location="main")

if st.session_state["authentication_status"] == False:
    st.error("Username/password Incorrect")
if st.session_state["authentication_status"]:
    authenticator.logout(location="main")
    # Page Style CSS
    css = """
    <style>
        .h_1 {
            font-size: 14px;
        }
        .h_1_value {
            font-size: 12px;
            font-weight: bold;
        }
        .active_heading{
            text-align:center; 
            padding:10px;
            background-color:green;
            margin-bottom:50px;
            border-radius:10px;
            color:white;
            font-size:15px;
            font-weight:bold;
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
          font-size: 10px;
          font-family: Arial, sans-serif;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          box-sizing: border-box;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Header Section
    st.markdown(
        """
        <div style='text-align:center; padding-top:20px;'>
            <h1 style='font-size:48px; margin-bottom:0;'>Dhammi Enterprises</h1>
            <p style='font-size:22px; color:gray;'>Upload Estate</p>
        </div>
        """, unsafe_allow_html=True)

    # Enable Geo Location via Device
    use_geolocation = st.checkbox("Enable Your Geolocation")
    if use_geolocation:
        geo_location = streamlit_geolocation()
    # Add New Real Estate
    with st.form("property_form"):
        left, right = st.columns(2)
        property_uuid = str(uuid.uuid4())
        location = left.text_input("Name of Real Estate Location", placeholder="eg. Locality Name, District etc.")
        exact_plot_number = right.text_input("Exact Plot Number", placeholder="eg. D-123")
        direction = right.text_input("Facing Direction of Real Estate", placeholder="eg. North Facing, South Facing")
        price_per_gaz = left.number_input("Price/Sq Yd", value=None, placeholder="0")
        area_size_in_gaz = right.number_input("Area in Sq Yd", value=None, placeholder="0")
        description = left.text_area("Description of Real Estate",
                                     placeholder="eg. Good location, Extra Society Charges")
        image = right.file_uploader("Upload Image of Real Estate", type=["jpg", "jpeg", "png", "heic", "heif"])
        lat = None
        lng = None
        if use_geolocation:
            lat = geo_location.get("latitude")
            lng = geo_location.get("longitude")
            st.write(f"Latitude: {lat}")
            st.write(f"Longitude: {lng}")
        else:
            lat = left.number_input("Latitude", format="%.6f", value=None)
            lng = left.number_input("Longitude", format="%.6f", value=None)
        uploading_date = right.datetime_input("Date of Uploading", value=datetime.now())
        reference = st.text_input("Property Reference Person/Contact Details",
                                  placeholder="eg. dealer A, contact XX-XXX-XXX")
        submitted = st.form_submit_button("Upload")
        if submitted:
            data = {
                "uuid": property_uuid,
                "location": location,
                "exact_plot_number": exact_plot_number,
                "direction": direction,
                "price_per_gaz": price_per_gaz if price_per_gaz else 0,
                "area_size_in_gaz": area_size_in_gaz if area_size_in_gaz else 0,
                "description": description,
                "image": Binary(image.read()) if image else None,
                "latitude": lat,
                "longitude": lng,
                "uploading_date": uploading_date,
                "reference": reference}
            mongo.addData("real_estates", data)
            st.success("Property added successfully!")
    st.markdown("---")

    # Sub-Header Section
    st.markdown(
        """
        <div class=active_heading>
            Active Real Estates
        </div>
        """, unsafe_allow_html=True)

    # All Listed Properties Edit/Delete
    with st.spinner("Loading Data..."):
        properties = mongo.getAllData(MONGO_DB_REAL_ESTATE_TABLE)
    for property in properties:
        col1, col2 = st.columns([1, 2])
        with col1:
            try:
                st.image(property.get("image", "https://dummyimage.com/600x400.png"))
            except:
                st.image("https://dummyimage.com/600x400.png")
        with col2:
            try:
                dt = property.get("uploading_date", None)
                day = dt.day
                property_content = f"""
                    <div style="display: flex;">
                        <div class=container>
                            <div style='font-weight:bold; font-size:16px;'>📍{property.get('location', None)}</div>
                            <div> ↗ {property.get('direction', None)}</div>
                        </div>
                        <div style="margin-left:auto;">Ph. +91 {CONTACT_NUMBER}</div>
                    </div>
                    <div class=container>
                        <div style="background-color:#b8b8b8;margin:10px;padding: 10px;border-radius: 12px">Exact Plot Number: {property.get('exact_plot_number', None)}</div>
                        <div> <b>Uploaded On:</b><br>{dt.strftime(f"%-I:%M%p, {day} %B %Y")}</div>
                    </div>
                    <div class=container>
                        <div class=box style='min-width:20%'>
                           <div class=h_1 >🏷 Price<br> </div>
                            <div class=h_1_value>{format_currency(property.get('price_per_gaz', 0), 'INR', '#,##,##0', locale='en_IN', currency_digits=False)}/Sq Yd </div>
                        </div>
                        <div class=box>
                            <div class=h_1> ⎕ Area<br> </div>
                            <div class=h_1_value>{format_decimal(property.get('area_size_in_gaz', 0), locale='en_IN')} Sq Yd </div>
                        </div>
                        <div class=box>
                            <div class=h_1>🟰 Total Costing<br></div>
                            <div class=h_1_value>{format_currency(property.get('price_per_gaz', 0) * property.get('area_size_in_gaz', 0), 'INR', '#,##,##0', locale='en_IN', currency_digits=False)}</div>
                        </div>
                    </div>
                    
                    <div class=container style='gap:0px;'>
                        <div class=box><b>Description:</b><br>{property.get("description", None)}</div>
                        <div class=box><b>Geo Co-ordinates:</b><br>{property.get("latitude", None)}, {property.get("longitude", None)}</div>
                        <div class=box><b>Reference:</b><br>{property.get("reference", None)}</div>
                    </div>
                """
                st.markdown(property_content, unsafe_allow_html=True)
            except Exception as e:
                print(e)


            # Pop Up Window for Editing
            @st.dialog("Edit Real Estate")
            def edit(property):
                left, right = st.columns(2)
                property_uuid = property["uuid"]
                location = left.text_input("Name of Real Estate Location", value=property.get("location", None))
                exact_plot_number = right.text_input("Exact Plot Number", value=property.get("exact_plot_number", None))
                direction = right.text_input("Direction in which Real Estate is Facing",
                                             value=property.get("direction", None))
                price_per_gaz = left.number_input("Price/Sq Yd", value=property.get("price_per_gaz", 0))
                area_size_in_gaz = right.number_input("Area in Sq Yd", value=property.get("area_size_in_gaz", 0))
                description = left.text_area("Description of Real Estate", value=property.get("description", None))
                image = right.file_uploader("Upload Image of Real Estate",
                                            type=["jpg", "jpeg", "png", "heic", "heif"])
                lat = left.number_input("Latitude", format="%.6f", value=property.get("latitude", None))
                lng = left.number_input("Longitude", format="%.6f", value=property.get("longitude", None))
                reference = st.text_input("Property Reference Person/Contact Details",
                                          value=property.get("reference", None))
                # Button to Update the Data
                if st.button("Update"):
                    data = {
                        "uuid": property_uuid,
                        "location": location,
                        "exact_plot_number": exact_plot_number,
                        "direction": direction,
                        "price_per_gaz": price_per_gaz,
                        "area_size_in_gaz": area_size_in_gaz,
                        "description": description,
                        "image": Binary(image.read()) if image else property.get("image", None),
                        "latitude": lat,
                        "longitude": lng,
                        "reference": reference}
                    mongo.updateData("real_estates", property["uuid"], data)
                    st.success("Property Updated Successfully!")
                    time.sleep(1)
                    st.rerun()


            @st.dialog("Confirm the Delete Action!")
            def confirmDelete(property):
                if st.button("Confirm Delete", key=f"{property["uuid"]}_confirm"):
                    mongo.deleteData("real_estates", property["uuid"])
                    st.rerun()
        # Edit Button
        if st.button("Edit", key=f"{property['uuid']}_edit", use_container_width=True):
            edit(property)
        # Delete Button
        if st.button("Delete", key=property["uuid"], use_container_width=True):
            confirmDelete(property)
        # Separator
        st.markdown("---")
