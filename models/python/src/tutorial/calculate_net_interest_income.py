#  Copyright 2022 Accenture Global Solutions Limited
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import decimal
import typing as tp

import pandas as pd
import tracdap.rt.api as trac
import schemas as schemas

class EarningAssetsDataModel(trac.TracModel):

    def define_parameters(self) -> tp.Dict[str, trac.ModelParameter]:

        return trac.define_parameters(

            trac.P("expected_base_rate", trac.FLOAT,
                   label="expected base rate"),

            trac.P("expected_employee_cost_change", trac.FLOAT,
                   label="expected employee cost change")
                   )

    def define_inputs(self) -> tp.Dict[str, trac.ModelInputSchema]:
        earning_assets = trac.load_schema(schemas, "interest_earning_assets.csv")
        return {"interest_earning_assets": trac.ModelInputSchema(earning_assets)}

    def define_outputs(self) -> tp.Dict[str, trac.ModelOutputSchema]:
        emmisions = trac.load_schema(schemas, "financed_emmisions.csv")
        return {"financed_emmisions": trac.ModelInputSchema(emmisions)}

    def run_model(self, ctx: trac.TracContext):
        ctx.log().info("Financed_emmisions model is running...")

        expected_base_rate = ctx.get_parameter("expected_base_rate")
        expected_employee_cost_change = ctx.get_parameter("expected_employee_cost_change")

        earning_assets = ctx.get_pandas_table("interest_earning_assets")
        # dummy computations
        financed_emmisions = earning_assets.rename(columns={"average_balance":"financed_emmisions"})
        ctx.put_pandas_table("financed_emmisions", financed_emmisions)

if __name__ == "__main__":
    import tracdap.rt.launch as launch
    launch.launch_model(EarningAssetsDataModel, "config/financed_emmisions.yaml", "config/sys_config.yaml")
