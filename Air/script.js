function getAQI() {
    const city = document.getElementById("cityInput").value; // Get city input

    fetch(`http://127.0.0.1:5001/predict?city=${city}`, {  // CORRECT backend URL
        method: "GET",
        mode: "cors"
    })
    .then(response => response.json())
    .then(data => {
        console.log("AQI Data:", data); // Log data for debugging

        // Display the result in the HTML
        if (data.error) {
            document.getElementById("result").innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            document.getElementById("result").innerHTML = `
                <h3>Air Quality Index (AQI) for ${city}</h3>
                <p><strong>AQI Bucket:</strong> ${data.AQI_Bucket}</p>
                <h4>Pollution Levels:</h4>
                <ul>
                    <li>PM10: ${data.Pollution_Levels.PM10}</li>
                    <li>NO: ${data.Pollution_Levels.NO}</li>
                    <li>NO2: ${data.Pollution_Levels.NO2}</li>
                    <li>O3: ${data.Pollution_Levels.O3}</li>
                    <li>SO2: ${data.Pollution_Levels.SO2}</li>
                    <li>NH3: ${data.Pollution_Levels.NH3}</li>
                    <li>CO: ${data.Pollution_Levels.CO}</li>
                    <li>PM2.5: ${data.Pollution_Levels["PM2.5"]}</li>
                </ul>
            `;
        }
    })
    .catch(error => {
        console.error("Error fetching AQI data:", error);
        document.getElementById("result").innerHTML = `<p>Error fetching AQI data.</p>`;
    });
}
