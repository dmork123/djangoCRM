import random
from django.shortcuts import reverse
from django.views import generic
from .mixins import OrganisorAndLoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from django.core.mail import send_mail


class AgentListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organization = self.request.user.userprofile, # User that created this agent
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM. PLease come login to start working",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    form_class = AgentModelForm
    context_object_name = "agent"
    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organisation)

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organisation)

class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organisation)



