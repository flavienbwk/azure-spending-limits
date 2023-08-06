# Azure Spending Limits

Minimal configuration to set soft **and hard** limits on Microsoft Azure to avoid overspending with a "Pay-as-you-go" account.

Some examples of why it's useful :

- Avoid unexpected API consumption spending (such as infinite loops)
- Avoid cost for forgotten VMs or resources

The provided script will delete the services in a resource group with an action group. It won't delete the resource group, which is convenient. Also, this is a last resort solution as it will require you to reconfigure your services after removal.

_This method is probably not the best but is "quick" to setup and just works. You might prefer [rate-limiting](https://techcommunity.microsoft.com/t5/azure-paas-blog/configure-rate-limits-for-different-api-operations-in-azure-api/ba-p/3789108) API calls, or trigger an action group on a [carefully analyzed spending](https://learn.microsoft.com/en-us/answers/questions/931661/how-can-i-find-how-much-per-hour-i-am-being-billed) (spoiler: this is hard)._

## How to set soft and hard limits

Remember that accumulated cost showing in your "Cost Management" console is an estimate only. Real cost may [take time to update](https://learn.microsoft.com/en-us/azure/azure-monitor/usage-estimated-costs) and is generally stabilized one day after a resource is consumed. However, it is possible to set hard limits based on [forecasted cost](https://learn.microsoft.com/en-us/azure/cost-management-billing/finops/capabilities-forecasting).

This schema represents the steps to set soft and hard limits on a resource group :

![Schema of the workflow configured to delete resources when a spending limit is reached.](./delete-resource-workflow-azure.jpg)
