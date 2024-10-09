import streamlit as st

def hover():
    tooltip_html = """
        <style>
        #tooltip {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 250px;
            background-color: #e6f3f3;
            color: black;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            cursor: pointer;
        }
        </style>

        <div id="tooltip" onclick="hideTooltip()">
            Would you like to leave us feedback?<br>
            Just type <code>/feedback</code> at the beginning of your message!<br>
            (example: <code>/feedback awesome app!</code>)
        </div>

        <script>
        function hideTooltip() {
            document.getElementById('tooltip').style.display = 'none';
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
        }
        </script>
        """

    st.components.v1.html(tooltip_html, height=100)