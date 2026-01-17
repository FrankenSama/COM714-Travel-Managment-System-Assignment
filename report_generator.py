# FILE: report_generator.py
import matplotlib.pyplot as plt
import os
from datetime import datetime
from typing import List, Tuple
from collections import defaultdict
import numpy as np

class ReportGenerator:
    REPORTS_DIR = "reports"
    
    @staticmethod
    def _ensure_reports_dir():
        """Ensure reports directory exists."""
        os.makedirs(ReportGenerator.REPORTS_DIR, exist_ok=True)
    
    @staticmethod
    def generate_trip_statistics(trips: List) -> Tuple[bool, str]:
        """Generate trip statistics report with bar chart."""
        ReportGenerator._ensure_reports_dir()
        
        if not trips:
            return False, "No trip data available for statistics."
        
        # Group trips by coordinator
        coordinators = {}
        active_trips = 0
        inactive_trips = 0
        
        for trip in trips:
            if trip.coordinator:
                coord_name = trip.coordinator.name
                coordinators[coord_name] = coordinators.get(coord_name, 0) + 1
            
            if trip.is_active:
                active_trips += 1
            else:
                inactive_trips += 1
        
        if not coordinators:
            return False, "No coordinator data available."
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # First subplot: Trips per Coordinator
        bars = ax1.bar(coordinators.keys(), coordinators.values(), color='steelblue')
        ax1.set_title('Trips per Coordinator', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Coordinator', fontsize=12)
        ax1.set_ylabel('Number of Trips', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Second subplot: Active vs Inactive Trips
        pie_data = [active_trips, inactive_trips]
        pie_labels = [f'Active ({active_trips})', f'Inactive ({inactive_trips})']
        colors = ['#66c2a5', '#fc8d62']
        
        ax2.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('Trip Status Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        filename = f"trip_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(ReportGenerator.REPORTS_DIR, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return True, filepath
    
    @staticmethod
    def generate_financial_summary(invoices: List) -> Tuple[bool, str]:
        """Generate financial summary report with visualizations."""
        ReportGenerator._ensure_reports_dir()
        
        if not invoices:
            return False, "No invoice data available."
        
        # Calculate financial metrics
        total_revenue = sum(inv.total_amount for inv in invoices)
        total_paid = sum(sum(p.amount for p in inv.payments) for inv in invoices)
        total_outstanding = total_revenue - total_paid
        
        paid_count = sum(1 for inv in invoices if inv.is_fully_paid())
        pending_count = len(invoices) - paid_count
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Subplot 1: Revenue Overview (Bar Chart)
        categories = ['Total Revenue', 'Total Paid', 'Outstanding']
        values = [total_revenue, total_paid, total_outstanding]
        colors = ['#8dd3c7', '#80b1d3', '#fb8072']
        
        bars = ax1.bar(categories, values, color=colors)
        ax1.set_title('Financial Overview', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Amount (£)', fontsize=12)
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'£{height:.2f}', ha='center', va='bottom')
        
        # Subplot 2: Invoice Status (Pie Chart)
        status_data = [paid_count, pending_count]
        status_labels = [f'Paid ({paid_count})', f'Pending ({pending_count})']
        status_colors = ['#66c2a5', '#fc8d62']
        
        ax2.pie(status_data, labels=status_labels, autopct='%1.1f%%', 
                colors=status_colors, startangle=90)
        ax2.set_title('Invoice Status', fontsize=14, fontweight='bold')
        
        # Subplot 3: Payment Methods Distribution
        payment_methods = defaultdict(float)
        for invoice in invoices:
            for payment in invoice.payments:
                payment_methods[payment.method] += payment.amount
        
        if payment_methods:
            methods = list(payment_methods.keys())
            amounts = list(payment_methods.values())
            ax3.barh(methods, amounts, color='lightcoral')
            ax3.set_title('Payment Methods', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Amount (£)', fontsize=12)
            
            for i, v in enumerate(amounts):
                ax3.text(v, i, f' £{v:.2f}', va='center')
        else:
            ax3.text(0.5, 0.5, 'No payment data', ha='center', va='center', 
                    transform=ax3.transAxes)
            ax3.set_title('Payment Methods', fontsize=14, fontweight='bold')
        
        # Subplot 4: Top Invoices by Value
        sorted_invoices = sorted(invoices, key=lambda x: x.total_amount, reverse=True)[:5]
        
        if sorted_invoices:
            invoice_labels = [f"{inv.trip.name[:20]}..." if len(inv.trip.name) > 20 
                            else inv.trip.name for inv in sorted_invoices]
            invoice_amounts = [inv.total_amount for inv in sorted_invoices]
            
            bars = ax4.barh(invoice_labels, invoice_amounts, color='skyblue')
            ax4.set_title('Top 5 Invoices by Value', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Amount (£)', fontsize=12)
            
            for i, v in enumerate(invoice_amounts):
                ax4.text(v, i, f' £{v:.2f}', va='center')
        else:
            ax4.text(0.5, 0.5, 'No invoice data', ha='center', va='center',
                    transform=ax4.transAxes)
            ax4.set_title('Top 5 Invoices by Value', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        filename = f"financial_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(ReportGenerator.REPORTS_DIR, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return True, filepath
    
    @staticmethod
    def generate_traveller_statistics(travellers: List) -> Tuple[bool, str]:
        """Generate traveller statistics report."""
        ReportGenerator._ensure_reports_dir()
        
        if not travellers:
            return False, "No traveller data available."
        
        # Calculate age distribution
        current_year = datetime.now().year
        age_groups = {'0-18': 0, '19-30': 0, '31-50': 0, '51-70': 0, '70+': 0}
        
        for traveller in travellers:
            age = current_year - traveller.date_of_birth.year
            if age <= 18:
                age_groups['0-18'] += 1
            elif age <= 30:
                age_groups['19-30'] += 1
            elif age <= 50:
                age_groups['31-50'] += 1
            elif age <= 70:
                age_groups['51-70'] += 1
            else:
                age_groups['70+'] += 1
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Subplot 1: Age Distribution
        groups = list(age_groups.keys())
        counts = list(age_groups.values())
        colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3']
        
        bars = ax1.bar(groups, counts, color=colors)
        ax1.set_title('Traveller Age Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Age Group', fontsize=12)
        ax1.set_ylabel('Number of Travellers', fontsize=12)
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Subplot 2: Total Travellers Overview
        total_travellers = len(travellers)
        ax2.text(0.5, 0.6, f'Total Travellers', ha='center', va='center',
                fontsize=16, fontweight='bold', transform=ax2.transAxes)
        ax2.text(0.5, 0.4, f'{total_travellers}', ha='center', va='center',
                fontsize=48, fontweight='bold', color='steelblue',
                transform=ax2.transAxes)
        ax2.axis('off')
        
        plt.tight_layout()
        
        filename = f"traveller_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(ReportGenerator.REPORTS_DIR, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return True, filepath
    
    @staticmethod
    def generate_revenue_trends(invoices: List, trips: List) -> Tuple[bool, str]:
        """Generate revenue trends report."""
        ReportGenerator._ensure_reports_dir()
        
        if not invoices:
            return False, "No invoice data available for trends."
        
        # Group invoices by month
        monthly_revenue = defaultdict(float)
        monthly_trips = defaultdict(int)
        
        for invoice in invoices:
            month_key = invoice.issue_date.strftime('%Y-%m')
            monthly_revenue[month_key] += invoice.total_amount
        
        for trip in trips:
            month_key = trip.start_date.strftime('%Y-%m')
            monthly_trips[month_key] += 1
        
        # Sort by date
        sorted_months = sorted(monthly_revenue.keys())
        
        if len(sorted_months) < 2:
            return False, "Insufficient data for trend analysis (need at least 2 months)."
        
        revenues = [monthly_revenue[month] for month in sorted_months]
        trip_counts = [monthly_trips.get(month, 0) for month in sorted_months]
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Subplot 1: Revenue Trend
        ax1.plot(sorted_months, revenues, marker='o', linewidth=2, 
                color='steelblue', markersize=8)
        ax1.fill_between(range(len(sorted_months)), revenues, alpha=0.3, color='steelblue')
        ax1.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Month', fontsize=12)
        ax1.set_ylabel('Revenue (£)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(revenues):
            ax1.text(i, v, f'£{v:.0f}', ha='center', va='bottom')
        
        # Subplot 2: Trips Trend
        ax2.bar(sorted_months, trip_counts, color='lightcoral', alpha=0.7)
        ax2.set_title('Monthly Trip Count', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Month', fontsize=12)
        ax2.set_ylabel('Number of Trips', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(trip_counts):
            ax2.text(i, v, f'{int(v)}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        filename = f"revenue_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(ReportGenerator.REPORTS_DIR, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return True, filepath

print("Report Generator module loaded successfully.")