# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------


# EXAMPLE: IntegrationRuntimes_Create
def step_integrationruntimes_create(test, rg):
    test.cmd('az datafactory integration-runtime self-hosted create '
             '--factory-name "{myFactoryName}" '
             '--description "A selfhosted integration runtime" '
             '--name "{myIntegrationRuntime}" '
             '--resource-group "{rg}"',
             checks=[])


def step_triggerruns_rerun(test, rg):
    test.cmd('az datafactory trigger-run rerun '
             '--factory-name "{myFactoryName}" '
             '--resource-group "{rg}" '
             '--trigger-name "{myTrigger}" '
             '--run-id "{myRunId}"',
             checks=[])


def step_pipelines_createrun(test, rg):
    output = test.cmd('az datafactory pipeline create-run '
                      '--factory-name "{myFactoryName}" '
                      '--parameters "{{\\"OutputBlobNameList\\":[\\"exampleoutput.csv\\"]}}" '
                      '--name "{myPipeline}" '
                      '--resource-group "{rg}"',
                      checks=[]).get_output_in_json()
    return output


def step_triggerruns_querybyfactory(test, rg):
    output = test.cmd('az datafactory trigger-run query-by-factory '
                      '--factory-name "{myFactoryName}" '
                      '--last-updated-after "{myStartTime}" '
                      '--last-updated-before "{myEndTime}" '
                      '--resource-group "{rg}"',
                      checks=[]).get_output_in_json()
    return output


def step_integrationruntimes_managed_create(test, rg):
    test.cmd('az datafactory integration-runtime managed create '
             '--factory-name "{myFactoryName}" '
             '--name "{myIntegrationRuntime}" '
             '--resource-group "{rg}" '
             '--description "Managed Integration Runtime" '
             '--type-properties-compute-properties "{{\\"location\\":'
             '\\"East US 2\\",\\"nodeSize\\":\\"Standard_D2_v3\\",'
             '\\"numberOfNodes\\":1,\\"maxParallelExecutionsPerNode\\":2}}" '
             '--type-properties-ssis-properties "{{\\"edition\\":\\"Standard'
             '\\",\\"licenseType\\":\\"LicenseIncluded\\"}}" ',
             checks=[])


def step_pipelines_wait_create(test, rg):
    test.cmd('az datafactory pipeline create '
             '--factory-name "{myFactoryName}" '
             '--pipeline "{{\\"activities\\":[{{\\"name\\":\\"Wait1\\",'
             '\\"type\\":\\"Wait\\",\\"dependsOn\\":[],\\"userProperties'
             '\\":[],\\"typeProperties\\":{{\\"waitTimeInSeconds\\":5'
             '}}}}],\\"annotations\\":[]}}" '
             '--name "{myPipeline}" '
             '--resource-group "{rg}" ',
             checks=[])


def step_triggers_tumble_create(test, rg):
    test.cmd('az datafactory trigger create '
             '--resource-group "{rg}" '
             '--properties "{{\\"description\\":\\"trumblingwindowtrigger'
             '\\",\\"annotations\\":[],\\"pipeline\\":{{\\"pipelineReference'
             '\\":{{\\"referenceName\\":\\"{myPipeline}\\",\\"type\\":'
             '\\"PipelineReference\\"}}}},\\"type\\":\\"TumblingWindowTrigger'
             '\\",\\"typeProperties\\":{{\\"frequency\\":\\"Minute\\",'
             '\\"interval\\":5,\\"startTime\\":\\"{myStartTime}\\",'
             '\\"endTime\\":\\"{myEndTime}\\",\\"delay\\":\\"00:00:00\\",'
             '\\"maxConcurrency\\":50,\\"retryPolicy\\":{{\\"intervalInSeconds'
             '\\":30}},\\"dependsOn\\":[]}}}}" '
             '--factory-name "{myFactoryName}" '
             '--name "{myTrigger}"',
             checks=[])


def call_managed_integrationruntime_scenario(test, rg):
    from ....tests.latest import test_datafactory_scenario as g
    g.setup(test, rg)
    g.step_factories_createorupdate(test, rg)
    step_integrationruntimes_managed_create(test, rg)
    g.step_integrationruntimes_get(test, rg)
    g.step_integrationruntimes_start(test, rg)
    g.step_integrationruntimes_stop(test, rg)
    g.step_integrationruntimes_delete(test, rg)
    g.step_factories_delete(test, rg)
    g.cleanup(test, rg)


def call_triggerrun_scenario(test, rg):
    from ....tests.latest import test_datafactory_scenario as g
    import time
    g.setup(test, rg)
    g.step_factories_createorupdate(test, rg)
    step_pipelines_wait_create(test, rg)
    createrun_res = g.step_pipelines_createrun(test, rg)
    time.sleep(5)
    test.kwargs.update({'myRunId': createrun_res.get('runId')})
    g.step_pipelineruns_get(test, rg)
    g.step_activityruns_querybypipelinerun(test, rg)
    createrun_res = g.step_pipelines_createrun(test, rg)
    test.kwargs.update({'myRunId': createrun_res.get('runId')})
    g.step_pipelineruns_cancel(test, rg)
    step_triggers_tumble_create(test, rg)
    g.step_triggers_start(test, rg)
    g.step_triggers_get(test, rg)
    maxRound = 2
    while True:
        triggerrun_res = g.step_triggerruns_querybyfactory(test, rg)
        if len(triggerrun_res['value']) > 0 and triggerrun_res['value'][0]['status'] == 'Succeeded':
            test.kwargs.update({'myRunId': triggerrun_res['value'][0]['triggerRunId']})
            break
        else:
            if maxRound > 0:
                maxRound -= 1
                print("waiting round: " + str(5 - maxRound))
                time.sleep(300)
            else:
                break
    if maxRound > 0:
        g.step_triggerruns_rerun(test, rg)
    g.step_triggerruns_querybyfactory(test, rg)
    g.step_triggers_stop(test, rg)
    g.step_triggers_delete(test, rg)
    g.step_pipelines_delete(test, rg)
    g.step_factories_delete(test, rg)


def call_main_scenario(test, rg):
    from ....tests.latest import test_datafactory_scenario as g
    g.setup(test, rg)
    g.step_factories_createorupdate(test, rg)
    g.step_factories_update(test, rg)
    g.step_linkedservices_create(test, rg)
    g.step_linkedservices_update(test, rg)
    g.step_datasets_create(test, rg)
    g.step_datasets_update(test, rg)
    g.step_pipelines_create(test, rg)
    g.step_pipelines_update(test, rg)
    g.step_triggers_create(test, rg)
    g.step_triggers_update(test, rg)
    g.step_integrationruntimes_create(test, rg)
    g.step_integrationruntimes_update(test, rg)
    g.step_pipelines_createrun(test, rg)
    g.step_integrationruntimes_get(test, rg)
    g.step_reruntriggers_listbytrigger(test, rg)
    g.step_linkedservices_get(test, rg)
    # g.step_pipelineruns_get(test, rg)
    g.step_pipelines_get(test, rg)
    g.step_datasets_get(test, rg)
    g.step_triggers_get(test, rg)
    g.step_integrationruntimes_listbyfactory(test, rg)
    g.step_linkedservices_listbyfactory(test, rg)
    g.step_pipelines_listbyfactory(test, rg)
    g.step_triggers_listbyfactory(test, rg)
    g.step_datasets_listbyfactory(test, rg)
    g.step_factories_get(test, rg)
    g.step_factories_listbyresourcegroup(test, rg)
    g.step_factories_list(test, rg)
    g.step_operations_list(test, rg)
    # g.step_reruntriggers_cancel(test, rg)
    # g.step_reruntriggers_start(test, rg)
    # g.step_reruntriggers_stop(test, rg)
    g.step_integrationruntimes_regenerateauthkey(test, rg)
    # g.step_triggerruns_rerun(test, rg)
    # g.step_integrationruntimes_getconnectioninfo(test, rg)
    g.step_integrationruntimes_synccredentials(test, rg)
    g.step_integrationruntimes_getmonitoringdata(test, rg)
    g.step_integrationruntimes_listauthkeys(test, rg)
    g.step_integrationruntimes_upgrade(test, rg)
    g.step_integrationruntimes_getstatus(test, rg)
    # g.step_integrationruntimes_start(test, rg)
    # g.step_integrationruntimes_stop(test, rg)
    # g.step_integrationruntimes_createlinkedintegrationruntime(test, rg)
    g.step_triggers_geteventsubscriptionstatus(test, rg)
    # g.step_activityruns_querybypipelinerun(test, rg)
    g.step_triggers_unsubscribefromevents(test, rg)
    g.step_triggers_subscribetoevents(test, rg)
    g.step_triggers_start(test, rg)
    g.step_triggers_stop(test, rg)
    # g.step_factories_getgithubaccesstoken(test, rg)
    g.step_factories_getdataplaneaccess(test, rg)
    # g.step_pipelineruns_querybyfactory(test, rg)
    # g.step_pipelineruns_cancel(test, rg)
    g.step_triggerruns_querybyfactory(test, rg)
    g.step_factories_configurefactoryrepo(test, rg)
    g.step_integrationruntimes_delete(test, rg)
    g.step_triggers_delete(test, rg)
    g.step_pipelines_delete(test, rg)
    g.step_datasets_delete(test, rg)
    g.step_linkedservices_delete(test, rg)
    g.step_factories_delete(test, rg)
    g.cleanup(test, rg)


def call_scenario(test, rg):
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    startTime = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    an_hour_later = now + timedelta(hours=1)
    endTime = an_hour_later.strftime("%Y-%m-%dT%H:%M:%SZ")
    test.kwargs.update({
        'myStartTime': startTime,
        'myEndTime': endTime
    })
    call_main_scenario(test, rg)
    call_managed_integrationruntime_scenario(test, rg)
    call_triggerrun_scenario(test, rg)
