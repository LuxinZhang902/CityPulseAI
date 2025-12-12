"""
PDF Report Generator for CityPulse AI
Creates comprehensive reports with charts, insights, and analysis.
"""

import os
import io
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

class PDFReportGenerator:
    """Generate professional PDF reports for CityPulse AI analysis."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom styles for the PDF report."""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1e40af'),
            alignment=TA_CENTER
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#3b82f6'),
            alignment=TA_LEFT
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            textColor=colors.black
        )
        
        # Insight style
        self.insight_style = ParagraphStyle(
            'CustomInsight',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=20,
            textColor=colors.HexColor('#1f2937')
        )
    
    def generate_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate a complete PDF report from analysis data."""
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Build story (content)
        story = []
        
        # Title page
        story.extend(self._create_title_page(analysis_data))
        
        # Executive Summary
        story.extend(self._create_executive_summary(analysis_data))
        
        # Key Insights
        story.extend(self._create_key_insights(analysis_data))
        
        # Risk Assessment
        story.extend(self._create_risk_assessment(analysis_data))
        
        # Recommendations
        story.extend(self._create_recommendations(analysis_data))
        
        # Charts and Visualizations
        story.extend(self._create_charts_section(analysis_data))
        
        # Data Analysis
        story.extend(self._create_data_analysis(analysis_data))
        
        # Technical Details
        story.extend(self._create_technical_details(analysis_data))
        
        # Build PDF
        doc.build(story)
        
        # Save PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"citypulse_report_{timestamp}.pdf"
        filepath = f"reports/{filename}"
        
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(buffer.getvalue())
        
        buffer.close()
        return filepath
    
    def _create_title_page(self, data: Dict[str, Any]) -> List:
        """Create title page content."""
        story = []
        
        # Main title
        story.append(Paragraph("CityPulse AI Analysis Report", self.title_style))
        story.append(Spacer(1, 20))
        
        # Query
        query = data.get('query', 'Emergency Data Analysis')
        story.append(Paragraph(f"<b>Query:</b> {query}", self.subtitle_style))
        story.append(Spacer(1, 10))
        
        # Metadata
        metadata = [
            ['Generated:', datetime.now().strftime("%B %d, %Y at %I:%M %p")],
            ['Analysis Type:', data.get('analysis_type', 'Comprehensive Analysis').replace('_', ' ').title()],
            ['Data Source:', 'SnowLeopard AI' if data.get('snowleopard_solution') else 'Local Database'],
            ['Records Analyzed:', str(len(data.get('raw_rows', [])))],
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 3*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 30))
        
        return story
    
    def _create_executive_summary(self, data: Dict[str, Any]) -> List:
        """Create executive summary section."""
        story = []
        
        story.append(Paragraph("Executive Summary", self.subtitle_style))
        
        # Get comprehensive analysis or fallback
        comprehensive = data.get('comprehensive_analysis', {})
        summary = comprehensive.get('executive_summary', data.get('insight_summary', 'Analysis completed successfully.'))
        
        story.append(Paragraph(summary, self.body_style))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_key_insights(self, data: Dict[str, Any]) -> List:
        """Create key insights section."""
        story = []
        
        story.append(Paragraph("Key Insights", self.subtitle_style))
        
        # Get insights from comprehensive analysis or fallback
        comprehensive = data.get('comprehensive_analysis', {})
        insights = comprehensive.get('key_insights', data.get('key_insights', []))
        
        if not insights:
            insights = ['Analysis completed successfully', 'Data patterns identified', 'Recommendations generated']
        
        for i, insight in enumerate(insights, 1):
            story.append(Paragraph(f"{i}. {insight}", self.insight_style))
        
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_risk_assessment(self, data: Dict[str, Any]) -> List:
        """Create risk assessment section."""
        story = []
        
        story.append(Paragraph("Risk Assessment", self.subtitle_style))
        
        # Get risk assessment from comprehensive analysis
        comprehensive = data.get('comprehensive_analysis', {})
        risk_assessment = comprehensive.get('risk_assessment', {})
        
        risk_level = risk_assessment.get('level', 'MEDIUM')
        risk_reasoning = risk_assessment.get('reasoning', 'Based on current data patterns and distribution.')
        
        # Risk level with color
        risk_colors = {
            'LOW': colors.green,
            'MEDIUM': colors.orange,
            'HIGH': colors.red,
            'CRITICAL': colors.HexColor('#dc2626')
        }
        
        risk_color = risk_colors.get(risk_level.upper(), colors.black)
        
        story.append(Paragraph(f"<b>Risk Level:</b> <font color='{risk_color.hex() if hasattr(risk_color, 'hex') else '#000000'}'>{risk_level.upper()}</font>", self.body_style))
        story.append(Paragraph(f"<b>Assessment:</b> {risk_reasoning}", self.body_style))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_recommendations(self, data: Dict[str, Any]) -> List:
        """Create recommendations section."""
        story = []
        
        story.append(Paragraph("Recommendations", self.subtitle_style))
        
        # Get recommendations from comprehensive analysis
        comprehensive = data.get('comprehensive_analysis', {})
        recommendations = comprehensive.get('recommendations', [])
        
        if not recommendations:
            recommendations = [
                'Monitor high-frequency areas for resource allocation',
                'Consider temporal patterns for emergency response planning',
                'Implement data-driven decision making processes'
            ]
        
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", self.insight_style))
        
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_charts_section(self, data: Dict[str, Any]) -> List:
        """Create charts and visualizations section."""
        story = []
        
        story.append(Paragraph("Data Visualizations", self.subtitle_style))
        
        # Generate charts from chart data
        chart_data = data.get('chart_data', {})
        charts = chart_data.get('charts', [])
        
        if charts:
            for chart in charts[:3]:  # Limit to 3 charts
                try:
                    chart_image = self._create_chart_image(chart)
                    if chart_image:
                        story.append(Paragraph(chart.get('title', 'Chart'), self.styles['Heading3']))
                        story.append(chart_image)
                        story.append(Paragraph(chart.get('description', ''), self.body_style))
                        story.append(Spacer(1, 20))
                except Exception as e:
                    print(f"Error creating chart: {e}")
                    continue
        else:
            story.append(Paragraph("No chart data available for this analysis.", self.body_style))
            story.append(Spacer(1, 20))
        
        return story
    
    def _create_chart_image(self, chart: Dict[str, Any]) -> Optional[Image]:
        """Create a chart image and return as ReportLab Image."""
        try:
            chart_type = chart.get('type', 'bar')
            chart_data = chart.get('data', {})
            labels = chart_data.get('labels', [])
            values = chart_data.get('values', [])
            
            if not labels or not values:
                return None
            
            # Create matplotlib figure
            plt.figure(figsize=(8, 5))
            
            if chart_type == 'bar':
                plt.bar(labels, values, color='#3b82f6')
                plt.xticks(rotation=45, ha='right')
            elif chart_type == 'pie':
                plt.pie(values, labels=labels, autopct='%1.1f%%')
            elif chart_type == 'line':
                plt.plot(labels, values, marker='o', color='#3b82f6', linewidth=2)
                plt.xticks(rotation=45, ha='right')
            
            plt.title(chart.get('title', 'Data Chart'), fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            # Save to buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Create ReportLab Image
            chart_image = Image(img_buffer, width=6*inch, height=3.75*inch)
            return chart_image
            
        except Exception as e:
            print(f"Error creating chart image: {e}")
            return None
    
    def _create_data_analysis(self, data: Dict[str, Any]) -> List:
        """Create data analysis section."""
        story = []
        
        story.append(Paragraph("Data Analysis Details", self.subtitle_style))
        
        # Top neighborhoods
        neighborhoods = data.get('top_neighborhoods', [])
        if neighborhoods:
            story.append(Paragraph("Top Affected Areas", self.styles['Heading3']))
            
            neighborhood_data = [['Rank', 'Neighborhood', 'Count', 'Percentage']]
            total = sum(n.get('count', 0) for n in neighborhoods)
            
            for i, neighborhood in enumerate(neighborhoods[:10], 1):
                name = neighborhood.get('name', 'Unknown')
                count = neighborhood.get('count', 0)
                percentage = (count / total * 100) if total > 0 else 0
                neighborhood_data.append([str(i), name, str(count), f"{percentage:.1f}%"])
            
            neighborhood_table = Table(neighborhood_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch])
            neighborhood_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
            ]))
            
            story.append(neighborhood_table)
            story.append(Spacer(1, 20))
        
        return story
    
    def _create_technical_details(self, data: Dict[str, Any]) -> List:
        """Create technical details section."""
        story = []
        
        story.append(Paragraph("Technical Details", self.subtitle_style))
        
        # SQL Query
        sql_used = data.get('sql_used', 'No SQL query available')
        story.append(Paragraph("Generated SQL Query", self.styles['Heading3']))
        story.append(Paragraph(f"<font name='Courier'>{sql_used}</font>", self.body_style))
        story.append(Spacer(1, 12))
        
        # SQL Explanation
        sql_explanation = data.get('sql_explanation', 'No explanation available')
        story.append(Paragraph("Query Explanation", self.styles['Heading3']))
        story.append(Paragraph(sql_explanation, self.body_style))
        story.append(Spacer(1, 12))
        
        # Technical Details
        technical_details = data.get('technical_details', '')
        if technical_details:
            story.append(Paragraph("Technical Information", self.styles['Heading3']))
            story.append(Paragraph(technical_details, self.body_style))
        
        # Data Source
        sql_source = data.get('sql_source', 'Unknown')
        story.append(Paragraph(f"<b>Data Source:</b> {sql_source}", self.body_style))
        
        return story

# Singleton instance
pdf_generator = PDFReportGenerator()
