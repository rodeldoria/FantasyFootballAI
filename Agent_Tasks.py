from crewai import Task

class Agent_Tasks:
    def handle_incident_task(self, agent):
        return Task(
            role='Handle Incident',
            agent=agent,
            goal='Resolve IT incidents efficiently',
            description='Investigate and resolve IT incidents to minimize disruption to services.',
            expected_output='Resolved incidents and improved service continuity.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def manage_change_task(self, agent):
        return Task(
            role='Manage Change',
            agent=agent,
            goal='Coordinate and implement IT changes',
            description='Plan, coordinate, and implement IT changes to minimize disruption and ensure successful deployments.',
            expected_output='Successful IT changes and minimal disruption to services.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def support_service_desk_task(self, agent):
        return Task(
            role='Support Service Desk',
            agent=agent,
            goal='Provide IT support to users',
            description='Help users resolve IT issues efficiently and provide effective assistance.',
            expected_output='Resolved user issues and improved support services.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def manage_problem_task(self, agent, dependencies):
        return Task(
            role='Manage Problem',
            agent=agent,
            goal='Identify and resolve root causes of IT problems',
            description='Investigate and resolve underlying causes of IT issues to prevent recurrence.',
            expected_output='Resolved problems and reduced recurrence of incidents.',
            dependencies=dependencies,
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def manage_release_task(self, agent):
        return Task(
            role='Manage Release',
            agent=agent,
            goal='Plan and execute IT releases',
            description='Plan, schedule, and manage IT releases to ensure successful deployment.',
            expected_output='Successful IT releases and minimal deployment issues.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def manage_asset_task(self, agent):
        return Task(
            role='Manage Asset',
            agent=agent,
            goal='Oversee IT asset management',
            description='Manage the lifecycle of IT assets to ensure efficient use and proper retirement.',
            expected_output='Optimized IT asset usage and accurate asset records.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def manage_configuration_task(self, agent):
        return Task(
            role='Manage Configuration',
            agent=agent,
            goal='Oversee IT configuration management',
            description='Maintain accurate IT configuration records to support other ITSM processes.',
            expected_output='Accurate and up-to-date configuration records.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def handle_case_task(self, agent):
        return Task(
            role='Handle Case',
            agent=agent,
            goal='Manage IT cases effectively',
            description='Handle IT cases efficiently and document all related information.',
            expected_output='Resolved IT cases and well-documented case records.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )

    def manage_service_catalog_task(self, agent):
        return Task(
            role='Manage Service Catalog',
            agent=agent,
            goal='Maintain the IT service catalog',
            description='Ensure the IT service catalog is up-to-date and accurately reflects available services.',
            expected_output='Up-to-date and accurate IT service catalog.',
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )
