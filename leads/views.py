from django.core.mail import send_mail
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Agent, Lead
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")
    
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def lead_landing_page(request):
    return render(request, "landing.html")

# converted a function based view to class based


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    # since no context is past, in our html file its default value would be object_list
    context_object_name = "leads"  # Though we can update that to what we want here

    def get_queryset(self):
        user = self.request.user
        
        # initial queryset of leads for the entire organisation 
        if user.is_organisor: # if a user is an organisor then they will have a userProfile.
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user) # https://youtu.be/fOukA4Qh9QA?t=20972 
        
        return queryset # this is where it makes the final call to the DB
    
    # exmaple of how you would pass context in a class based view      
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data( **kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True) # The agent__isnull filter to see if that foreignkey object is null
            context.update({
                "unassigned_leads": queryset
            })
        return context
            
        
def lead_list(request):
    leads = Lead.objects.all()

    context = {
        "leads": leads
    }

    return render(request, "leads/lead_list.html", context=context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    # since no context is past, in our html file its default value would be object_list
    context_object_name = "lead"  # Though we can update that to what we want here
    
    def get_queryset(self):
        user = self.request.user
        
        # initial queryset of leads for the entire organisation 
        if user.is_organisor: # if a user is an organisor then they will have a userProfile.
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user) # https://youtu.be/fOukA4Qh9QA?t=20972 
        
        return queryset # this is where it makes the final call to the DB


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self) -> str:
        return reverse("leads:lead-list")

    def form_valid(self, form):

        send_mail(subject="A lead has been created", message="Go to the site to see the new lead",
                  from_email="test@test.com", recipient_list=["test2@test.com"])
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        print("Reciving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            print("the Lead has been created")
            return redirect("/leads")

    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        
        return Lead.objects.filter(organization=user.userprofile) # this is where it makes the final call to the DB

    def get_success_url(self) -> str:
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            print("the Lead has been updated")
            return redirect("/leads")

    context = {
        "lead": lead,
        "form": form
    }
    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user
        
        # initial queryset of leads for the entire organisation 
        if user.is_organisor: # if a user is an organisor then they will have a userProfile.
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user) # https://youtu.be/fOukA4Qh9QA?t=20972 
        
        return queryset # this is where it makes the final call to the DB



    def get_success_url(self) -> str:
        return reverse("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         print("Reciving a post request")
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             print("The form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             print("the Lead has been created")
#             return redirect("/leads")

#     context={
#         "lead": lead,
#         "form": form
#     }
#     return render(request, "leads/lead_update.html", context)

# def lead_create(request):
    # form = LeadForm()
    # if request.method == "POST":
    #     print("Reciving a post request")
    #     form = LeadModelForm(request.POST)
    #     if form.is_valid():
    #         print("The form is valid")
    #         print(form.cleaned_data)
    #         first_name = form.cleaned_data["first_name"]
    #         last_name = form.cleaned_data["last_name"]
    #         age = form.cleaned_data["age"]
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         print("the Lead has been created")
    #         return redirect("/leads")

#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)
