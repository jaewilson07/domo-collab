
    @staticmethod
    def _generate_prompt_prompt_refiner( ):
        return Message(
                "SYSTEM", f"""
        You are a Prompt Engineer. Your job is to refine prompts for use by AI agents.

        EXAMPLE
            "unrefined_prompt": "researching leads and creating personalized email drafts for the sales team",
            "refined_prompt":  "As a member of the sales team at company, your mission is to explore the digital landscape for potential leads. 
            Equipped with advanced tools and a strategic approach, you analyze data, trends, and interactions to discover opportunities that others might miss. 
            Your efforts are vital in creating pathways for meaningful engagements and driving the companys growth. 
            Your goal is to identify high-value leads that align with our ideal customer profile. 
            Perform a thorough analysis of lead_company, a company that has recently shown interest in our solutions. 
            Use all available data sources to create a detailed profile, concentrating on key decision-makers, recent business developments, and potential needs that match our offerings. 
            This task is essential for effectively customizing our engagement strategy."

            ADDITIONAL INSTRUCTIONS        
            Avoid making assumptions and only use information you are certain about.      
            """
        )

    def llm_refine_prompt(self, prompt):
        messages = Messages([
            self._generate_prompt_prompt_refiner()
            Message("USER", 
                    """refine this prompt.  
                    unrefined_prompt:{prompt}
                    
                    ADDITIONAL_INSTRUCTIONS:
                    only return the refined prompt as a string
                    """
            )
        ])

        res = self.invoke(messages = messages)
        return res



    @staticmethod
    def _llm_dataflow_process_definition(res: rgd.ResponseGetData):
        return {
            "dataflow_id": res.response["id"],
            "dataflow_name": res.response["name"],
            "datafow_actions": res.response["actions"],
        }
    def llm_describe_dataflow(
        self,
        dataflow_id,
        messages: Messages = None,
        debug_api: bool = False,
        return_raw: bool = False,
    ):

        res = dataset_routes.get_dataflow_by_id_sync(
            auth=self.auth, dataflow_id=dataflow_id, debug_api=debug_api
        )

        data = self._llm_dataflow_process_definition(res)

        messages = Messages(
            [
                Message(
                    "SYSTEM",
                    "you are an interpreter that translates a json definition of a data transformation process into plain english for business users.",
                )
            ]
        )
        prompt = Message(
            "USER",
            f"""
                         describe the following JSON transformation steps in plain english: {data}.
                         
                         Limit your response to 100 words
                         """,
        )

        messages.messages.append(prompt)

        res = self.invoke(messages=messages, debug_api=debug_api, return_raw=return_raw)

        res.messages = messages

        return res
