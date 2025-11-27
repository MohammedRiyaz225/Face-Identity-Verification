rom flask import Flask, render_template, request, jsonify
import random
from datetime import datetime
import numpy as np  # For AI risk assessment
import re  # For text processing

app = Flask(__name__)


# AI risk assessment model (simplified)
class SafetyRiskModel:
    def __init__(self):
        # Pre-defined risk factors for different countries and regions (simplified AI knowledge base)
        self.country_risk_factors = {
            "afghanistan": 0.9, "australia": 0.2, "brazil": 0.5, "canada": 0.2,
            "china": 0.4, "egypt": 0.6, "france": 0.3, "germany": 0.2,
            "india": 0.5, "italy": 0.3, "japan": 0.2, "mexico": 0.6,
            "russia": 0.6, "spain": 0.3, "thailand": 0.4, "ukraine": 0.8,
            "united kingdom": 0.3, "united states": 0.4, "venezuela": 0.7
        }

        # Risk factors for different types of regions
        self.region_modifiers = {
            "city": 0.1,  # Urban areas might have slightly higher risks
            "rural": -0.05,  # Rural areas often have lower crime
            "coastal": 0.03,  # Coastal areas might have weather risks
            "mountain": 0.05,  # Mountain regions have terrain risks
            "border": 0.15  # Border regions can have higher risks
        }

        # Season-based risk factors (simplified)
        self.current_month = datetime.now().month
        self.seasonal_risks = {
            # Hurricane/typhoon seasons, winter travel risks, etc.
            "north_summer": [6, 7, 8, 9],
            "north_winter": [12, 1, 2, 3],
            "monsoon": [6, 7, 8, 9]
        }

    def get_base_country_risk(self, country):
        """Get base risk score for a country"""
        country = country.lower()
        # Direct match
        if country in self.country_risk_factors:
            return self.country_risk_factors[country]

        # Partial match
        for known_country, risk in self.country_risk_factors.items():
            if known_country in country or country in known_country:
                return risk

        # Default moderate risk for unknown countries
        return 0.5

    def analyze_seasonal_risk(self, country):
        """Analyze seasonal risk factors"""
        country = country.lower()
        risk_modifier = 0

        # Northern hemisphere summer risks (hurricanes, etc.)
        if self.current_month in self.seasonal_risks["north_summer"]:
            if country in ["united states", "mexico", "japan", "china", "philippines"]:
                risk_modifier += 0.1  # Hurricane/typhoon risk

        # Northern hemisphere winter risks
        if self.current_month in self.seasonal_risks["north_winter"]:
            if country in ["canada", "russia", "norway", "sweden", "finland", "iceland"]:
                risk_modifier += 0.15  # Severe winter conditions

        # Monsoon season
        if self.current_month in self.seasonal_risks["monsoon"]:
            if country in ["india", "thailand", "vietnam", "myanmar", "bangladesh"]:
                risk_modifier += 0.2  # Flood risks

        return risk_modifier

    def analyze_location_context(self, country, city):
        """Analyze specific location context for risks"""
        city = city.lower() if city else ""
        context_modifier = 0

        # Check for high-risk cities
        high_risk_cities = ["caracas", "kabul", "mogadishu", "damascus"]
        moderate_risk_cities = ["rio de janeiro", "johannesburg", "nairobi", "karachi"]

        if any(city.find(high_city) >= 0 for high_city in high_risk_cities):
            context_modifier += 0.2
        elif any(city.find(mod_city) >= 0 for mod_city in moderate_risk_cities):
            context_modifier += 0.1

        # Region type analysis
        for region_type, modifier in self.region_modifiers.items():
            if region_type in city or region_type in country:
                context_modifier += modifier

        return context_modifier

    def assess_risk(self, country, city=""):
        """Main method to assess overall risk and generate intelligent alerts"""
        if not country:
            return {"risk_score": 0.5, "confidence": 0.3, "factors": ["insufficient data"]}

        # Get base country risk
        base_risk = self.get_base_country_risk(country)

        # Add seasonal factors
        seasonal_risk = self.analyze_seasonal_risk(country)

        # Add location context
        context_risk = self.analyze_location_context(country, city)

        # Calculate overall risk (with bounds)
        overall_risk = min(max(base_risk + seasonal_risk + context_risk, 0.1), 0.95)

        # Determine confidence level based on available data
        confidence = 0.8 if country in self.country_risk_factors else 0.5
        confidence = confidence - 0.1 if not city else confidence

        # Identify risk factors
        factors = []
        if base_risk > 0.6:
            factors.append("general country advisory")
        if seasonal_risk > 0.05:
            factors.append("seasonal weather conditions")
        if context_risk > 0.05:
            factors.append("specific location risks")

        # If no specific factors but risk is elevated
        if not factors and overall_risk > 0.4:
            factors.append("combined risk factors")

        return {
            "risk_score": overall_risk,
            "confidence": confidence,
            "factors": factors
        }


# AI recommendation engine
class TravelRecommendationEngine:
    def __init__(self):
        self.safety_phrases = [
            "Stay aware of your surroundings at all times",
            "Keep emergency contacts readily available",
            "Register with your embassy before traveling",
            "Research local laws and customs before your trip",
            "Keep copies of important documents",
            "Share your itinerary with someone you trust",
            "Avoid displaying valuable items in public",
            "Use reputable transportation services",
            "Stay in well-reviewed accommodations",
            "Maintain communication with friends and family"
        ]

        self.high_risk_recommendations = [
            "Consider postponing non-essential travel",
            "Maintain low profile and avoid crowds",
            "Prepare emergency evacuation plans",
            "Check in regularly with your embassy",
            "Limit movements to daylight hours in unfamiliar areas"
        ]

        self.weather_recommendations = {
            "storm": ["Secure loose objects", "Stay indoors during severe weather", "Keep emergency supplies ready"],
            "heat": ["Stay hydrated", "Avoid extended exposure during peak hours", "Know signs of heat illness"],
            "cold": ["Dress in layers", "Be aware of icy conditions", "Carry emergency supplies in your vehicle"],
            "flood": ["Avoid flood-prone areas", "Never drive through standing water",
                      "Move to higher ground if needed"]
        }

    def generate_personalized_tips(self, country, city, risk_assessment):
        """Generate personalized safety recommendations"""
        risk_score = risk_assessment["risk_score"]
        risk_factors = risk_assessment["factors"]

        # Base recommendations everyone should follow
        recommendations = random.sample(self.safety_phrases, min(3, len(self.safety_phrases)))

        # Add high-risk recommendations if needed
        if risk_score > 0.6:
            recommendations.extend(
                random.sample(self.high_risk_recommendations, min(2, len(self.high_risk_recommendations))))

        # Add weather-specific recommendations
        current_month = datetime.now().month
        if "seasonal weather conditions" in risk_factors:
            # Northern hemisphere summer
            if current_month in [6, 7, 8]:
                if country.lower() in ["united states", "mexico", "caribbean"]:
                    recommendations.extend(random.sample(self.weather_recommendations["storm"], 1))
                if country.lower() in ["egypt", "india", "saudi arabia"]:
                    recommendations.extend(random.sample(self.weather_recommendations["heat"], 1))
            # Northern hemisphere winter
            elif current_month in [12, 1, 2]:
                if country.lower() in ["canada", "russia", "sweden", "norway"]:
                    recommendations.extend(random.sample(self.weather_recommendations["cold"], 1))
            # Monsoon season
            if current_month in [6, 7, 8, 9] and country.lower() in ["india", "thailand", "vietnam"]:
                recommendations.extend(random.sample(self.weather_recommendations["flood"], 1))

        return recommendations


# Initialize our AI models
risk_model = SafetyRiskModel()
recommendation_engine = TravelRecommendationEngine()


# Create a simple index.html template
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Travel Safety Bot</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { padding: 20px; background-color: pink; }
            .card { margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .alert-high { background-color: #f8d7da; }
            .alert-medium { background-color: #fff3cd; }
            .alert-low { background-color: #d1ecf1; }
            .risk-meter { height: 10px; border-radius: 5px; margin: 10px 0; background: linear-gradient(to right, green, yellow, red); }
            .risk-indicator { width: 10px; height: 20px; background-color: #000; position: relative; top: -15px; border-radius: 2px; }
            .recommendations { background-color: #e7f5ff    ; padding: 15px; border-radius: 5px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4 text-center">AI Travel Safety Bot</h1>

            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>Search Location</h5>
                        </div>
                        <div class="card-body">
                            <form id="searchForm">
                                <div class="mb-3">
                                    <label for="country" class="form-label">Country</label>
                                    <input type="text" class="form-control" id="country" required>
                                </div>
                                <div class="mb-3">
                                    <label for="city" class="form-label">City (Optional)</label>
                                    <input type="text" class="form-control" id="city">
                                </div>
                                <button type="submit" class="btn btn-primary">Get AI Safety Analysis</button>
                            </form>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>Alert Preferences</h5>
                        </div>
                        <div class="card-body">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="weatherAlerts" checked>
                                <label class="form-check-label" for="weatherAlerts">Weather Alerts</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="travelAdvisories" checked>
                                <label class="form-check-label" for="travelAdvisories">Travel Advisories</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="localIncidents" checked>
                                <label class="form-check-label" for="localIncidents">Local Incidents</label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>AI Safety Risk Assessment</h5>
                        </div>
                        <div class="card-body">
                            <div id="riskAssessment">
                                <div class="alert alert-info">
                                    Enter a location to get AI-powered safety assessment.
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>Safety Alerts</h5>
                        </div>
                        <div class="card-body">
                            <div id="alertsContainer">
                                <div class="alert alert-info">
                                    Search for a location to see AI-generated safety alerts.
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>AI Recommendations</h5>
                        </div>
                        <div class="card-body">
                            <div id="recommendationsContainer">
                                <div class="alert alert-info">
                                    Our AI will provide personalized safety recommendations based on your destination.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('searchForm').addEventListener('submit', function(e) {
                e.preventDefault();

                const country = document.getElementById('country').value;
                const city = document.getElementById('city').value;
                const weatherChecked = document.getElementById('weatherAlerts').checked;
                const advisoryChecked = document.getElementById('travelAdvisories').checked;
                const incidentsChecked = document.getElementById('localIncidents').checked;

                // Display loading indicators
                document.getElementById('riskAssessment').innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p>Analyzing risk factors...</p></div>';
                document.getElementById('alertsContainer').innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p>Generating alerts...</p></div>';
                document.getElementById('recommendationsContainer').innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p>Creating recommendations...</p></div>';

                fetch('/api/ai-analysis', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        country: country,
                        city: city,
                        filters: {
                            weather: weatherChecked,
                            advisory: advisoryChecked,
                            incident: incidentsChecked
                        }
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    // Display risk assessment
                    const riskScore = data.risk_assessment.risk_score;
                    const riskLevel = riskScore < 0.3 ? 'Low' : riskScore < 0.6 ? 'Medium' : 'High';
                    const riskColor = riskScore < 0.3 ? 'success' : riskScore < 0.6 ? 'warning' : 'danger';

                    let riskHTML = `
                        <div class="text-center mb-3">
                            <h3>Risk Level: <span class="text-${riskColor}">${riskLevel}</span></h3>
                            <p>AI Confidence: ${Math.round(data.risk_assessment.confidence * 100)}%</p>
                        </div>
                        <div class="risk-meter"></div>
                        <div class="risk-indicator" style="margin-left: ${riskScore * 100}%;"></div>
                        <div class="d-flex justify-content-between">
                            <small>Low Risk</small>
                            <small>Medium Risk</small>
                            <small>High Risk</small>
                        </div>
                        <div class="mt-3">
                            <p><strong>Risk Factors:</strong></p>
                            <ul>
                    `;

                    data.risk_assessment.factors.forEach(factor => {
                        riskHTML += `<li>${factor}</li>`;
                    });

                    riskHTML += `
                            </ul>
                        </div>
                    `;

                    document.getElementById('riskAssessment').innerHTML = riskHTML;

                    // Display safety alerts
                    const alertsContainer = document.getElementById('alertsContainer');

                    if (data.alerts.length === 0) {
                        alertsContainer.innerHTML = '<div class="alert alert-info">No alerts found for this location with current filters.</div>';
                    } else {
                        let alertsHTML = '';
                        data.alerts.forEach(alert => {
                            alertsHTML += `
                                <div class="alert alert-${alert.severity} mb-3">
                                    <div class="d-flex justify-content-between">
                                        <strong>${alert.title}</strong>
                                        <span class="badge bg-${getSeverityBadge(alert.severity)}">${alert.severity.toUpperCase()}</span>
                                    </div>
                                    <p class="mb-0 mt-2">${alert.description}</p>
                                    <small class="text-muted">Type: ${alert.type} | Source: ${alert.source || 'AI Analysis'}</small>
                                </div>
                            `;
                        });

                        alertsContainer.innerHTML = alertsHTML;
                    }

                    // Display recommendations
                    const recommendationsContainer = document.getElementById('recommendationsContainer');

                    let recsHTML = '<div class="recommendations"><h5>Personalized Safety Tips:</h5><ul>';
                    data.recommendations.forEach(rec => {
                        recsHTML += `<li>${rec}</li>`;
                    });
                    recsHTML += '</ul></div>';

                    recommendationsContainer.innerHTML = recsHTML;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('riskAssessment').innerHTML = '<div class="alert alert-danger">Error analyzing risks. Please try again.</div>';
                    document.getElementById('alertsContainer').innerHTML = '<div class="alert alert-danger">Error fetching alerts. Please try again.</div>';
                    document.getElementById('recommendationsContainer').innerHTML = '<div class="alert alert-danger">Error generating recommendations. Please try again.</div>';
                });
            });

            function getSeverityBadge(severity) {
                switch(severity) {
                    case 'high': return 'danger';
                    case 'medium': return 'warning';
                    case 'low': return 'info';
                    default: return 'secondary';
                }
            }
        </script>
    </body>
    </html>
    '''


# AI analysis endpoint
@app.route('/api/ai-analysis', methods=['POST'])
def ai_analysis():
    data = request.json
    country = data.get('country', '')
    city = data.get('city', '')
    filters = data.get('filters', {})

    # Use the AI risk model to assess safety risks
    risk_assessment = risk_model.assess_risk(country, city)

    # Generate personalized recommendations
    recommendations = recommendation_engine.generate_personalized_tips(country, city, risk_assessment)

    # Use risk assessment to generate intelligent alerts
    all_alerts = []
    risk_score = risk_assessment["risk_score"]

    # Determine number and severity of alerts based on risk score
    num_alerts = int(2 + risk_score * 5)  # 2-7 alerts based on risk

    # Add weather alerts if enabled
    if filters.get('weather', True):
        if risk_assessment["risk_score"] > 0.7:
            # Higher chance of severe weather alerts for high-risk areas
            severity = random.choices(['low', 'medium', 'high'], weights=[0.1, 0.3, 0.6])[0]
        else:
            severity = random.choices(['low', 'medium', 'high'], weights=[0.5, 0.3, 0.2])[0]

        # Generate weather alerts using more AI logic
        if "seasonal weather conditions" in risk_assessment["factors"]:
            month = datetime.now().month

            # Summer season in northern hemisphere
            if month in [6, 7, 8]:
                if country.lower() in ["united states", "mexico", "caribbean"]:
                    all_alerts.append({
                        'type': 'weather',
                        'severity': 'high' if risk_score > 0.6 else 'medium',
                        'title': 'Hurricane Risk Alert',
                        'description': f'Hurricane season active in {country}. Monitor local forecasts and have evacuation plan ready.',
                        'source': 'AI Weather Analysis',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
                elif country.lower() in ["india", "thailand", "vietnam", "philippines"]:
                    all_alerts.append({
                        'type': 'weather',
                        'severity': 'high' if risk_score > 0.7 else 'medium',
                        'title': 'Monsoon Season Alert',
                        'description': f'Heavy rainfall and potential flooding in {country}. Avoid low-lying areas and stay informed about weather conditions.',
                        'source': 'AI Weather Analysis',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
                elif country.lower() in ["egypt", "saudi arabia", "united arab emirates"]:
                    all_alerts.append({
                        'type': 'weather',
                        'severity': 'medium',
                        'title': 'Extreme Heat Warning',
                        'description': f'Dangerous heat levels in {country}. Limit outdoor activities, stay hydrated, and seek air-conditioned environments.',
                        'source': 'AI Temperature Analysis',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
            # Winter season in northern hemisphere
            elif month in [12, 1, 2]:
                if country.lower() in ["canada", "russia", "norway", "sweden", "finland"]:
                    all_alerts.append({
                        'type': 'weather',
                        'severity': 'medium',
                        'title': 'Winter Storm Alert',
                        'description': f'Severe winter conditions expected in {country}. Prepare for potential travel disruptions and power outages.',
                        'source': 'AI Weather Pattern Analysis',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })

            # Generic weather alert if no specific seasonal pattern matched
            if not any(alert['type'] == 'weather' for alert in all_alerts):
                all_alerts.append({
                    'type': 'weather',
                    'severity': severity,
                    'title': f'Weather Advisory for {country}',
                    'description': f'Variable weather conditions may affect travel plans in {city if city else country}. Monitor local forecasts.',
                    'source': 'AI Weather Analysis',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
        else:
            all_alerts.append({
                'type': 'weather',
                'severity': severity,
                'title': f'Weather Conditions in {country}',
                'description': f'No significant weather concerns identified for {city if city else country} at this time.',
                'source': 'AI Weather Analysis',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })

    # Add travel advisories if enabled
    if filters.get('advisory', True):
        # Base advisory on actual risk assessment
        if risk_score > 0.7:
            all_alerts.append({
                'type': 'advisory',
                'severity': 'high',
                'title': f'High-Risk Travel Advisory for {country}',
                'description': f'Exercise extreme caution when traveling to {city if city else country}. Consider postponing non-essential travel.',
                'source': 'AI Risk Analysis',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
        elif risk_score > 0.4:
            all_alerts.append({
                'type': 'advisory',
                'severity': 'medium',
                'title': f'Travel Advisory for {country}',
                'description': f'Exercise increased caution in {city if city else country} due to {random.choice(["political tensions", "crime concerns", "health risks"])}.',
                'source': 'AI Security Analysis',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
        else:
            all_alerts.append({
                'type': 'advisory',
                'severity': 'low',
                'title': f'General Travel Notice for {country}',
                'description': f'Normal security precautions advised when traveling to {city if city else country}.',
                'source': 'AI Advisory System',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })

        # Add special travel advisories based on known issues
        country_lower = country.lower()
        if country_lower in ["afghanistan", "syria", "yemen", "somalia"]:
            all_alerts.append({
                'type': 'advisory',
                'severity': 'high',
                'title': 'Extreme Risk Warning',
                'description': 'Avoid all travel to this destination due to armed conflict, terrorism risk, and kidnapping threat.',
                'source': 'AI Conflict Analysis',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
        elif city and city.lower() in ["rio de janeiro", "caracas", "kabul", "tijuana"]:
            all_alerts.append({
                'type': 'advisory',
                'severity': 'high',
                'title': f'City Safety Alert for {city}',
                'description': f'High crime rates reported in {city}. Avoid specific neighborhoods and exercise heightened awareness.',
                'source': 'AI Crime Pattern Analysis',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })

    # Add local incidents if enabled
    if filters.get('incident', True):
        # Generate incidents based on risk profile
        if risk_score > 0.6:
            # Higher likelihood of incidents in higher risk areas
            incident_count = random.randint(1, 3)
            incident_types = [
                ('Political Demonstration',
                 f'Planned protests in {city if city else "the capital"}. Avoid central areas and government buildings.'),
                ('Transportation Disruption',
                 f'Public transit strikes affecting {city if city else country}. Plan alternative transportation.'),
                ('Public Health Concern',
                 f'Localized disease outbreak reported. Follow proper hygiene measures and local health advisories.'),
                ('Security Operation',
                 f'Increased security presence in certain areas. Carry identification and comply with authorities.'),
                ('Civil Unrest',
                 f'Tensions reported in specific neighborhoods. Stay informed via local news and avoid affected areas.')
            ]

            for _ in range(incident_count):
                incident = random.choice(incident_types)
                all_alerts.append({
                    'type': 'incident',
                    'severity': 'medium' if risk_score > 0.7 else 'low',
                    'title': incident[0],
                    'description': incident[1],
                    'source': 'AI Incident Detection',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
        else:
            # Low risk areas have fewer incidents
            if random.random() < 0.5:  # 50% chance of having an incident in low-risk areas
                all_alerts.append({
                    'type': 'incident',
                    'severity': 'low',
                    'title': 'Minor Local Event',
                    'description': f'Small public gathering expected in {city if city else country}. No significant disruptions anticipated.',
                    'source': 'AI Event Analysis',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                })

    # Select a subset of alerts if we have too many
    if len(all_alerts) > num_alerts:
        # Prioritize higher severity alerts
        high_severity = [a for a in all_alerts if a['severity'] == 'high']
        medium_severity = [a for a in all_alerts if a['severity'] == 'medium']
        low_severity = [a for a in all_alerts if a['severity'] == 'low']

        selected_alerts = []
        selected_alerts.extend(high_severity)

        # Add medium severity until we reach the limit
        remaining = num_alerts - len(selected_alerts)
        if remaining > 0 and medium_severity:
            selected_alerts.extend(medium_severity[:min(remaining, len(medium_severity))])

        # Add low severity if still needed
        remaining = num_alerts - len(selected_alerts)
        if remaining > 0 and low_severity:
            selected_alerts.extend(low_severity[:min(remaining, len(low_severity))])
    else:
        selected_alerts = all_alerts

    return jsonify({
        'risk_assessment': risk_assessment,
        'alerts': selected_alerts,
        'recommendations': recommendations
    })


if __name__ == '__main__':
    app.run(debug=True)


