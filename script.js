
"use strict";

/* ============================================================
   MECHGUARD-AI
   Manual Sensor Input + AI Diagnosis
============================================================ */


/* ============================================================
   CONFIGURATION
============================================================ */

const API_BASE_URL = "http://127.0.0.1:5000";


/* ============================================================
   DOM ELEMENTS
============================================================ */

// Button
const diagnoseButton =
    document.getElementById("diagnose-machine-btn");

// System
const systemStatusDot =
    document.getElementById("system-status-dot");

const systemStatusText =
    document.getElementById("system-status-text");

// Machine
const machineStatus =
    document.getElementById("machine-status");

const machineOperatingHours =
    document.getElementById("machine-operating-hours");

// Health
const healthScoreValue =
    document.getElementById("health-score-value");

const healthScoreRing =
    document.getElementById("health-score-ring-fill");

// Risk
const heroRiskLabel =
    document.getElementById("hero-risk-label");

// Diagnosis
const predictedFault =
    document.getElementById("predicted-fault");

const diagnosisConfidence =
    document.getElementById("diagnosis-confidence");

const diagnosisRiskLevel =
    document.getElementById("diagnosis-risk-level");

const diagnosisRecommendation =
    document.getElementById("diagnosis-recommendation");

// Maintenance
const maintenancePriority =
    document.getElementById("maintenance-priority");

const maintenanceInspection =
    document.getElementById("maintenance-inspection");

const maintenanceLastCheck =
    document.getElementById("maintenance-last-check");

const maintenanceNextDue =
    document.getElementById("maintenance-next-due");

// Sensor inputs
const temperatureInput =
    document.getElementById("sensor-temperature-value");

const vibrationInput =
    document.getElementById("sensor-vibration-value");

const rpmInput =
    document.getElementById("sensor-rpm-value");

const loadInput =
    document.getElementById("sensor-load-value");

const currentInput =
    document.getElementById("sensor-current-value");

const hoursInput =
    document.getElementById("sensor-hours-value");


/* ============================================================
   NUMBER READER
============================================================ */

function readNumber(input, fieldName) {

    if (!input) {
        throw new Error(
            `${fieldName} input was not found.`
        );
    }


    const value =
        Number(input.value);


    if (!Number.isFinite(value)) {

        throw new Error(
            `${fieldName} must contain a valid number.`
        );
    }


    return value;
}


/* ============================================================
   READ MANUAL SENSOR INPUT
============================================================ */

function getSensorData() {

    const sensorData = {

        temperature_c:
            readNumber(
                temperatureInput,
                "Temperature"
            ),

        vibration_mm_s:
            readNumber(
                vibrationInput,
                "Vibration"
            ),

        rpm:
            readNumber(
                rpmInput,
                "RPM"
            ),

        load_percent:
            readNumber(
                loadInput,
                "Load"
            ),

        current_a:
            readNumber(
                currentInput,
                "Current"
            ),

        operating_hours:
            readNumber(
                hoursInput,
                "Operating Hours"
            )
    };


    console.log(
        "MANUAL SENSOR DATA:",
        sensorData
    );


    return sensorData;
}


/* ============================================================
   UPDATE SYSTEM STATUS
============================================================ */

function setSystemOnline() {

    if (systemStatusText) {

        systemStatusText.textContent =
            "SYSTEM ONLINE";
    }


    if (systemStatusDot) {

        systemStatusDot.classList.remove(
            "offline"
        );

        systemStatusDot.classList.add(
            "online"
        );
    }
}


function setSystemOffline() {

    if (systemStatusText) {

        systemStatusText.textContent =
            "SYSTEM OFFLINE";
    }


    if (systemStatusDot) {

        systemStatusDot.classList.remove(
            "online"
        );

        systemStatusDot.classList.add(
            "offline"
        );
    }
}


/* ============================================================
   CHECK FLASK BACKEND
============================================================ */

async function checkBackendStatus() {

    console.log(
        "Checking MECHGUARD-AI backend..."
    );


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/`
            );


        if (!response.ok) {

            throw new Error(
                "Backend returned an error."
            );
        }


        const data =
            await response.json();


        console.log(
            "Backend response:",
            data
        );


        setSystemOnline();


    } catch (error) {

        console.error(
            "Backend connection failed:",
            error
        );


        setSystemOffline();
    }
}


/* ============================================================
   UPDATE HEALTH SCORE
============================================================ */

function updateHealthScore(score) {

    if (!healthScoreValue) {
        return;
    }


    let health =
        Number(score);


    if (!Number.isFinite(health)) {
        health = 0;
    }


    health =
        Math.max(
            0,
            Math.min(
                100,
                Math.round(health)
            )
        );


    healthScoreValue.textContent =
        health;


    /* Circular progress */

    if (healthScoreRing) {

        const radius = 52;

        const circumference =
            2 * Math.PI * radius;

        const offset =
            circumference -
            (
                health / 100
            ) * circumference;


        healthScoreRing.style.strokeDasharray =
            `${circumference}`;

        healthScoreRing.style.strokeDashoffset =
            `${offset}`;

        healthScoreRing.style.transform =
            "rotate(-90deg)";

        healthScoreRing.style.transformOrigin =
            "60px 60px";
    }


    console.log(
        "Health score:",
        health
    );
}


/* ============================================================
   UPDATE FAULT
============================================================ */

function updateFault(fault) {

    if (!predictedFault) {
        return;
    }


    predictedFault.textContent =
        fault || "UNKNOWN";
}


/* ============================================================
   UPDATE CONFIDENCE
============================================================ */

function updateConfidence(confidence) {

    if (!diagnosisConfidence) {
        return;
    }


    let percentage;


    if (Number(confidence) <= 1) {

        percentage =
            Math.round(
                Number(confidence) * 100
            );

    } else {

        percentage =
            Math.round(
                Number(confidence)
            );
    }


    diagnosisConfidence.textContent =
        `${percentage}%`;


    console.log(
        "Confidence:",
        `${percentage}%`
    );
}


/* ============================================================
   UPDATE RISK
============================================================ */

function updateRisk(riskLevel) {

    const risk =
        String(
            riskLevel || "UNKNOWN"
        ).toUpperCase();


    /* Diagnosis badge */

    if (diagnosisRiskLevel) {

        diagnosisRiskLevel.textContent =
            risk;


        diagnosisRiskLevel.classList.remove(
            "badge--risk-low",
            "badge--risk-medium",
            "badge--risk-high"
        );


        if (risk === "LOW") {

            diagnosisRiskLevel.classList.add(
                "badge--risk-low"
            );

        } else if (risk === "MEDIUM") {

            diagnosisRiskLevel.classList.add(
                "badge--risk-medium"
            );

        } else if (risk === "HIGH") {

            diagnosisRiskLevel.classList.add(
                "badge--risk-high"
            );
        }
    }


    /* Hero risk */

    if (heroRiskLabel) {

        heroRiskLabel.textContent =
            `${risk} RISK`;


        heroRiskLabel.classList.remove(
            "risk-label--low",
            "risk-label--medium",
            "risk-label--high"
        );


        if (risk === "LOW") {

            heroRiskLabel.classList.add(
                "risk-label--low"
            );

        } else if (risk === "MEDIUM") {

            heroRiskLabel.classList.add(
                "risk-label--medium"
            );

        } else if (risk === "HIGH") {

            heroRiskLabel.classList.add(
                "risk-label--high"
            );
        }
    }


    console.log(
        "Risk:",
        risk
    );
}


/* ============================================================
   UPDATE RECOMMENDATION
============================================================ */

function updateRecommendation(action) {

    if (!diagnosisRecommendation) {
        return;
    }


    diagnosisRecommendation.textContent =
        action ||
        "No recommendation available.";
}


/* ============================================================
   UPDATE MACHINE STATUS
============================================================ */

function updateMachineStatus(result) {

    if (!machineStatus) {
        return;
    }


    const risk =
        String(
            result.risk_level || ""
        ).toUpperCase();


    if (risk === "HIGH") {

        machineStatus.textContent =
            "Attention Required";

    } else if (risk === "MEDIUM") {

        machineStatus.textContent =
            "Monitoring";

    } else {

        machineStatus.textContent =
            "Healthy";
    }


    /* Operating hours */

    if (
        machineOperatingHours &&
        hoursInput
    ) {

        const hours =
            Number(hoursInput.value);


        if (Number.isFinite(hours)) {

            machineOperatingHours.textContent =
                `${hours.toLocaleString()} h`;
        }
    }
}


/* ============================================================
   UPDATE MAINTENANCE
============================================================ */

function updateMaintenance(result) {

    const risk =
        String(
            result.risk_level || ""
        ).toUpperCase();


    const fault =
        String(
            result.fault_type || ""
        ).toUpperCase();


    /* ----------------------------------------
       Priority
    ---------------------------------------- */

    if (maintenancePriority) {

        let priority = "NORMAL";


        if (risk === "HIGH") {

            priority = "URGENT";

        } else if (risk === "MEDIUM") {

            priority = "MEDIUM";

        } else if (risk === "LOW") {

            priority = "LOW";
        }


        maintenancePriority.textContent =
            priority;


        maintenancePriority.classList.remove(
            "priority-low",
            "priority-medium",
            "priority-high"
        );


        if (risk === "HIGH") {

            maintenancePriority.classList.add(
                "priority-high"
            );

        } else if (risk === "MEDIUM") {

            maintenancePriority.classList.add(
                "priority-medium"
            );

        } else {

            maintenancePriority.classList.add(
                "priority-low"
            );
        }
    }


    /* ----------------------------------------
       Inspection
    ---------------------------------------- */

    if (maintenanceInspection) {

        if (fault === "OVERLOAD") {

            maintenanceInspection.textContent =
                "Inspect machine load and electrical current.";

        } else if (fault === "OVERHEATING") {

            maintenanceInspection.textContent =
                "Inspect cooling system and motor temperature.";

        } else if (fault === "BEARING_FAULT") {

            maintenanceInspection.textContent =
                "Inspect motor bearings and vibration levels.";

        } else if (fault === "MISALIGNMENT") {

            maintenanceInspection.textContent =
                "Inspect shaft alignment and coupling.";

        } else {

            maintenanceInspection.textContent =
                "Perform routine machine inspection.";
        }
    }


    /* ----------------------------------------
       Last check
    ---------------------------------------- */

    if (maintenanceLastCheck) {

        const now =
            new Date();


        maintenanceLastCheck.textContent =
            now.toLocaleString();
    }


    /* ----------------------------------------
       Next maintenance
    ---------------------------------------- */

    if (maintenanceNextDue) {

        let days = 30;


        if (risk === "HIGH") {

            days = 1;

        } else if (risk === "MEDIUM") {

            days = 7;

        } else if (risk === "LOW") {

            days = 30;
        }


        const nextDate =
            new Date();


        nextDate.setDate(
            nextDate.getDate() + days
        );


        maintenanceNextDue.textContent =
            nextDate.toLocaleDateString();
    }
}


/* ============================================================
   UPDATE COMPLETE DASHBOARD
============================================================ */

function updateDashboard(result) {

    console.log(
        "Updating dashboard..."
    );


    console.log(
        "AI RESULT:",
        result
    );


    /* Health */

    updateHealthScore(
        result.health_score
    );


    /* Fault */

    updateFault(
        result.fault_type
    );


    /* Confidence */

    updateConfidence(
        result.confidence
    );


    /* Risk */

    updateRisk(
        result.risk_level
    );


    /* Recommendation */

    updateRecommendation(
        result.recommended_action
    );


    /* Machine status */

    updateMachineStatus(
        result
    );


    /* Maintenance */

    updateMaintenance(
        result
    );


    console.log(
        "Dashboard updated successfully."
    );
}


/* ============================================================
   DIAGNOSE MACHINE
============================================================ */

async function diagnoseMachine() {

    console.log(
        "===================================="
    );

    console.log(
        "DIAGNOSE MACHINE"
    );

    console.log(
        "===================================="
    );


    try {

        /* ----------------------------------------
           Read manually entered values
        ---------------------------------------- */

        const sensorData =
            getSensorData();


        console.log(
            "Sending sensor data:",
            sensorData
        );


        /* ----------------------------------------
           Button loading
        ---------------------------------------- */

        if (diagnoseButton) {

            diagnoseButton.disabled =
                true;

            diagnoseButton.textContent =
                "ANALYZING...";
        }


        /* ----------------------------------------
           Send data to Flask
        ---------------------------------------- */

        const response =
            await fetch(
                `${API_BASE_URL}/api/diagnose`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            sensorData
                        )
                }
            );


        console.log(
            "API status:",
            response.status
        );


        /* ----------------------------------------
           Check API response
        ---------------------------------------- */

        if (!response.ok) {

            const errorText =
                await response.text();


            console.error(
                "API error:",
                errorText
            );


            throw new Error(
                `API Error: ${response.status}`
            );
        }


        /* ----------------------------------------
           Convert JSON
        ---------------------------------------- */

        const result =
            await response.json();


        console.log(
            "MECHGUARD-AI API RESPONSE:",
            result
        );


        /* ----------------------------------------
           UPDATE UI
        ---------------------------------------- */

        updateDashboard(
            result
        );


        /* Backend is working */

        setSystemOnline();


    } catch (error) {

        console.error(
            "Diagnosis failed:",
            error
        );


        /* ----------------------------------------
           Show error
        ---------------------------------------- */

        if (predictedFault) {

            predictedFault.textContent =
                "API ERROR";
        }


        if (diagnosisConfidence) {

            diagnosisConfidence.textContent =
                "--";
        }


        if (diagnosisRiskLevel) {

            diagnosisRiskLevel.textContent =
                "ERROR";
        }


        if (diagnosisRecommendation) {

            diagnosisRecommendation.textContent =
                "Unable to connect to the MECHGUARD-AI backend. Make sure Flask is running on port 5000.";
        }


        if (machineStatus) {

            machineStatus.textContent =
                "Connection Error";
        }


        setSystemOffline();


    } finally {

        /* ----------------------------------------
           Restore button
        ---------------------------------------- */

        if (diagnoseButton) {

            diagnoseButton.disabled =
                false;

            diagnoseButton.textContent =
                "DIAGNOSE MACHINE";
        }
    }
}


/* ============================================================
   DIAGNOSE BUTTON EVENT
============================================================ */

if (diagnoseButton) {

    diagnoseButton.addEventListener(
        "click",
        diagnoseMachine
    );

} else {

    console.error(
        "DIAGNOSE MACHINE button not found."
    );
}


/* ============================================================
   SIDEBAR NAVIGATION
============================================================ */

const sidebarLinks =
    document.querySelectorAll(
        ".sidebar__link"
    );


sidebarLinks.forEach(
    link => {

        link.addEventListener(
            "click",
            function () {

                sidebarLinks.forEach(
                    otherLink => {

                        const item =
                            otherLink.closest(
                                ".sidebar__item"
                            );


                        if (item) {

                            item.classList.remove(
                                "sidebar__item--active"
                            );
                        }
                    }
                );


                const currentItem =
                    this.closest(
                        ".sidebar__item"
                    );


                if (currentItem) {

                    currentItem.classList.add(
                        "sidebar__item--active"
                    );
                }
            }
        );
    }
);


/* ============================================================
   INITIALIZE DASHBOARD
============================================================ */

function initializeDashboard() {

    console.log(
        "===================================="
    );

    console.log(
        "MECHGUARD-AI DASHBOARD"
    );

    console.log(
        "Manual sensor mode enabled."
    );

    console.log(
        "===================================="
    );


    checkBackendStatus();
}


/* ============================================================
   START
============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);

