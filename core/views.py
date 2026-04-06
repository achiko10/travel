from django.views.generic import TemplateView, CreateView, DetailView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    SiteConfiguration, Category, Destination, Expedition, 
    FeaturedMedia, Booking, Article, QuickLead
)
from .forms import CustomUserCreationForm, BookingForm, QuickBookingForm
from .utils import send_telegram_notification, send_quick_lead_notification


# ── Mixin: injects 'site' into every template automatically ──────────────────
class SiteContextMixin:
    """Add this to any view to get {{ site }} in the template (footer, etc.)."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = SiteConfiguration.objects.first()
        return context


# ── Home ─────────────────────────────────────────────────────────────────────
class HomeView(SiteContextMixin, TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        location        = self.request.GET.get('location', '')
        category_id     = self.request.GET.get('category', '')
        tour_type       = self.request.GET.get('tour_type', '')
        max_price       = self.request.GET.get('max_price', '')
        search_date     = self.request.GET.get('date', '')
        duration_ranges = self.request.GET.getlist('duration')

        is_searching = bool(location or category_id or tour_type or search_date or duration_ranges or (max_price and max_price != '2500'))
        
        if is_searching:
            expeditions = Expedition.objects.all()
        else:
            expeditions = Expedition.objects.filter(is_featured=True)

        if location:
            expeditions = expeditions.filter(location__name__icontains=location)
        if category_id and category_id.isdigit():
            expeditions = expeditions.filter(category_id=category_id)
        if tour_type:
            expeditions = expeditions.filter(category__name__iexact=tour_type)
        # Only filter by price if the user explicitly moved the slider (not default)
        if max_price and max_price.isdigit():
            expeditions = expeditions.filter(price__lte=int(max_price))
        if duration_ranges:
            q_objects = Q()
            for r in duration_ranges:
                if r == '1-4':   q_objects |= Q(duration_days__range=[1, 4])
                elif r == '4-7': q_objects |= Q(duration_days__range=[4, 7])
                elif r == '7+':  q_objects |= Q(duration_days__gte=7)
            expeditions = expeditions.filter(q_objects)

        context['expeditions']         = expeditions
        context['categories']          = Category.objects.all()
        context['destinations']        = Destination.objects.filter(is_top_destination=True)
        context['featured_media']      = FeaturedMedia.objects.first()
        context['search_location']     = location
        context['search_category']     = category_id
        context['search_date']         = search_date
        # Show slider at max (2500) when no price filter active — so all tours visible
        context['search_max_price']    = max_price if max_price else '2500'
        context['search_durations']    = duration_ranges
        context['price_filter_active'] = bool(max_price)
        return context


# ── Expedition detail ─────────────────────────────────────────────────────────
class ExpeditionDetailView(SiteContextMixin, DetailView):
    model = Expedition
    template_name = 'core/expedition_detail.html'
    context_object_name = 'exp'


# ── Destination detail ────────────────────────────────────────────────────────
class DestinationDetailView(SiteContextMixin, DetailView):
    model = Destination
    template_name = 'core/destination_detail.html'
    context_object_name = 'dest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expeditions'] = Expedition.objects.filter(location=self.object)
        return context


# ── Checkout / Booking ────────────────────────────────────────────────────────
class CheckoutView(LoginRequiredMixin, View):
    """Accepts POST from expedition_detail booking form. Saves booking to DB."""

    def get(self, request, pk):
        # Direct GET visits (e.g. back-button) redirect to expedition page
        return redirect('expedition_detail', pk=pk)

    def post(self, request, pk):
        expedition = get_object_or_404(Expedition, pk=pk)
        form = BookingForm(request.POST)
        if form.is_valid():
            group_size = int(form.cleaned_data['group_size'])
            booking = Booking.objects.create(
                user=request.user,
                expedition=expedition,
                full_name=form.cleaned_data['full_name'],
                travel_date=form.cleaned_data['travel_date'],
                group_size=group_size,
                total_price=expedition.price * group_size,
            )
            
            # Send Telegram notification (asynchronously in a real app, 
            # but for this simple setup, we'll call it here)
            send_telegram_notification(booking)
            
            site = SiteConfiguration.objects.first()
            return render(request, 'core/checkout.html', {
                'exp': expedition,
                'booking': booking,
                'site': site,
            })
        # If form is invalid, redirect back to the expedition page
        return redirect('expedition_detail', pk=pk)


# ── Static / info pages ───────────────────────────────────────────────────────
class JournalView(SiteContextMixin, TemplateView):
    template_name = 'core/journal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context

class ArticleDetailView(SiteContextMixin, DetailView):
    model = Article
    template_name = 'core/article_detail.html'
    context_object_name = 'article'

class AboutView(SiteContextMixin, TemplateView):
    template_name = 'core/about.html'

class PrivacyView(SiteContextMixin, TemplateView):
    template_name = 'core/privacy.html'

class TermsView(SiteContextMixin, TemplateView):
    template_name = 'core/terms.html'


# ── Auth ──────────────────────────────────────────────────────────────────────
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class ProfileView(LoginRequiredMixin, SiteContextMixin, TemplateView):
    template_name = 'core/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = Booking.objects.filter(
            user=self.request.user
        ).select_related('expedition')
        context['bookings']       = bookings
        context['bookings_count'] = bookings.count()
        return context


# ── Custom error handlers ─────────────────────────────────────────────────────
def handler404(request, exception):
    site = SiteConfiguration.objects.first()
    return render(request, '404.html', {'site': site}, status=404)


class QuickBookingView(View):
    """Handles 'Quick Reservation' from home page Hero section."""

    def post(self, request):
        form = QuickBookingForm(request.POST)
        if form.is_valid():
            lead = QuickLead.objects.create(
                full_name=form.cleaned_data['full_name'],
                phone_number=form.cleaned_data['phone_number'],
                notes=form.cleaned_data['notes'],
            )
            # Notify owner
            send_quick_lead_notification(lead)
            
            # Simple success message for the user
            return render(request, 'core/checkout.html', {
                'quick_lead': lead,
                'site': SiteConfiguration.objects.first(),
                'is_success': True
            })
        return redirect('home')
