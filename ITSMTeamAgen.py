from crewai import Agent
# from tools.search_tools import SearchTools

class ITSMTeamAgents:
    def incident_manager_agent(self):
        return Agent(
            role='Incident Manager',
            goal='Handle and resolve IT incidents efficiently',
            backstory="""With extensive experience in incident management, you ensure all IT incidents are resolved promptly and effectively.""",
            allow_delegation=True,
            verbose=True,
            max_iter=15
        )

    def change_manager_agent(self):
        return Agent(
            role='Change Manager',
            goal='Manage IT changes efficiently',
            backstory="""You are responsible for managing and coordinating changes in the IT infrastructure, ensuring minimal disruption.""",
            allow_delegation=True,
            verbose=True,
            max_iter=15
        )

    def service_desk_agent(self):
        return Agent(
            role='Service Desk Agent',
            goal='Provide effective IT support',
            backstory="""You are the first point of contact for IT support, helping users resolve issues quickly and efficiently.""",
            # tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=True,
        )

    def problem_manager_agent(self):
        return Agent(
            role='Problem Manager',
            goal='Identify and resolve the root causes of IT problems',
            backstory="""With a deep understanding of problem management, you focus on identifying and eliminating the root causes of IT issues.""",
            verbose=True,
            allow_delegation=True,
        )

    def release_manager_agent(self):
        return Agent(
            role='Release Manager',
            goal='Plan and manage IT releases',
            backstory="""You are responsible for planning, scheduling, and controlling the build, test, and deployment of releases, ensuring successful delivery.""",
            verbose=True,
            allow_delegation=True,
        )

    def asset_manager_agent(self):
        return Agent(
            role='Asset Manager',
            goal='Manage IT assets efficiently',
            backstory="""You oversee the lifecycle of IT assets, ensuring they are used efficiently and retired appropriately.""",
            verbose=True,
            allow_delegation=True,
        )

    def configuration_manager_agent(self):
        return Agent(
            role='Configuration Manager',
            goal='Manage IT configurations',
            backstory="""You ensure that IT configurations are accurately recorded and maintained, supporting other ITSM processes.""",
            verbose=True,
            allow_delegation=True,
        )

    def case_manager_agent(self):
        return Agent(
            role='Case Manager',
            goal='Handle IT cases effectively',
            backstory="""You manage IT cases, ensuring that they are resolved efficiently and that all related information is properly documented.""",
            verbose=True,
            allow_delegation=True,
        )

    def service_catalog_manager_agent(self):
        return Agent(
            role='Service Catalog Manager',
            goal='Manage the IT service catalog',
            backstory="""You ensure that the IT service catalog is up-to-date and accurately reflects the services available to users.""",
            verbose=True,
            allow_delegation=True,
        )
