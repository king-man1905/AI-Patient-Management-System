console.log("Script Loaded");

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const token =
            localStorage.getItem(
                "token"
            );

        if (!token) {

            window.location.href =
                "/login";

            return;
        }

        const username =
            localStorage.getItem(
                "username"
            );

        if (
            username &&
            document.getElementById(
                "welcome-user"
            )
        ) {

            document.getElementById(
                "welcome-user"
            ).innerText =
                `Welcome ${username} 👋`;
        }

        loadHistory();

        const button =
            document.getElementById(
                "predict-btn"
            );

        button.addEventListener(
            "click",
            predictDiabetes
        );

    }
);

async function predictDiabetes() {

    const button =
        document.getElementById(
            "predict-btn"
        );

    const pregnancies =
        Number(
            document.getElementById(
                "pregnancies"
            ).value
        );

    const glucose =
        Number(
            document.getElementById(
                "glucose"
            ).value
        );

    const bloodPressure =
        Number(
            document.getElementById(
                "blood_pressure"
            ).value
        );

    const skinThickness =
        Number(
            document.getElementById(
                "skin_thickness"
            ).value
        );

    const insulin =
        Number(
            document.getElementById(
                "insulin"
            ).value
        );

    const bmi =
        Number(
            document.getElementById(
                "bmi"
            ).value
        );

    const dpf =
        Number(
            document.getElementById(
                "dpf"
            ).value
        );

    const age =
        Number(
            document.getElementById(
                "age"
            ).value
        );

    if (
        pregnancies < 0 ||
        glucose <= 0 ||
        bloodPressure <= 0 ||
        bmi <= 0 ||
        age <= 0
    ) {

        alert(
            "Please enter valid values"
        );

        return;
    }

    const token =
        localStorage.getItem(
            "token"
        );

    const data = {

        Pregnancies:
            pregnancies,

        Glucose:
            glucose,

        BloodPressure:
            bloodPressure,

        SkinThickness:
            skinThickness,

        Insulin:
            insulin,

        BMI:
            bmi,

        DiabetesPedigreeFunction:
            dpf,

        Age:
            age
    };

    try {

        button.disabled = true;

        button.innerText =
            "Predicting...";

        const response =
            await fetch(
                "/predict/",
                {
                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            "Bearer " +
                            token
                    },

                    body:
                        JSON.stringify(
                            data
                        )
                }
            );

        if (
            response.status === 401
        ) {

            localStorage.clear();

            window.location.href =
                "/login";

            return;
        }

        const result =
            await response.json();

        if (!response.ok) {

            document.getElementById(
                "result"
            ).innerText =
                result.detail ||
                "Prediction Failed";

            return;
        }

        const resultElement =
            document.getElementById(
                "result"
            );

        const recommendation =
            document.getElementById(
                "recommendation"
            );

        resultElement.innerText =
            result.result;

        if (
            result.result ===
            "Diabetic"
        ) {

            resultElement.style.color =
                "#ef4444";

            recommendation.innerText =
                "⚠️ Consult a healthcare professional and monitor glucose levels.";

        }

        else {

            resultElement.style.color =
                "#4ade80";

            recommendation.innerText =
                "✅ Maintain a healthy lifestyle and regular exercise.";
        }

        loadHistory();

    }

    catch(error) {

        console.log(error);

        document.getElementById(
            "result"
        ).innerText =
            "Server Error";
    }

    finally {

        button.disabled =
            false;

        button.innerText =
            "Predict Now";
    }
}

async function loadHistory() {

    try {

        const token =
            localStorage.getItem(
                "token"
            );

        const response =
            await fetch(
                "/predict/history",
                {
                    headers: {
                        "Authorization":
                            "Bearer " +
                            token
                    }
                }
            );

        if (
            response.status === 401
        ) {

            localStorage.clear();

            window.location.href =
                "/login";

            return;
        }

        const history =
            await response.json();

        const tableBody =
            document.getElementById(
                "history-body"
            );

        tableBody.innerHTML = "";

        let diabeticCount = 0;
        let healthyCount = 0;

        document.getElementById(
            "total-predictions"
        ).innerText =
            history.length;

        history.forEach(
            item => {

                if (
                    item.result ===
                    "Diabetic"
                ) {

                    diabeticCount++;

                } else {

                    healthyCount++;
                }

                const badge =
                    item.result ===
                    "Diabetic"

                    ? "🔴 Diabetic"

                    : "🟢 Healthy";

                tableBody.innerHTML += `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.glucose}</td>
                    <td>${badge}</td>
                </tr>
                `;
            }
        );

        updateChart(
            diabeticCount,
            healthyCount
        );

        const diabeticEl =
            document.getElementById(
                "diabetic-count"
            );

        const healthyEl =
            document.getElementById(
                "healthy-count"
            );

        if (diabeticEl) {

            diabeticEl.innerText =
                diabeticCount;
        }

        if (healthyEl) {

            healthyEl.innerText =
                healthyCount;
        }

    }

    catch(error) {

        console.log(
            "History Error:",
            error
        );
    }
}

function logout() {

    localStorage.clear();

    window.location.href =
        "/login";
}

let chart;

function updateChart(
    diabeticCount,
    healthyCount
){

    const ctx =
        document
        .getElementById(
            "predictionChart"
        );

    if(!ctx){
        return;
    }

    if(chart){
        chart.destroy();
    }

    chart =
    new Chart(
        ctx,
        {
            type:"doughnut",

            data:{
                labels:[
                    "Diabetic",
                    "Healthy"
                ],

                datasets:[
                    {
                        data:[
                            diabeticCount,
                            healthyCount
                        ],

                        backgroundColor:[
                            "#ef4444",
                            "#22c55e"
                        ]
                    }
                ]
            },

            options:{
                responsive:true,

                plugins:{
                    legend:{
                        labels:{
                            color:"white"
                        }
                    }
                }
            }
        }
    );
}