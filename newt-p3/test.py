import json
wrapper = {'error': '', 'status': 'OK', 'status_code': 200, 'output': {'MaxDiskWriteNode': {0: ''}, 'Partition': {0: 'work'}, 'MaxDiskReadNode': {0: ''}, 'AveDiskRead': {0: ''}, 'Elapsed': {0: '00:00:00'}, 'MinCPUTask': {0: ''}, 'MaxVMSize': {0: ''}, 'AveCPU': {0: ''}, 'MaxDiskRead': {0: ''}, 'AllocCPUS': {0: '48'}, 'ReqMem': {0: '0n'}, 'MinCPUNode': {0: ''}, 'MinCPU': {0: ''}, 'MaxVMSizeTask': {0: ''}, 'JobID': {0: '4803691'}, 'AvePages': {0: ''}, 'MaxPages': {0: ''}, 'ExitCode': {0: '0:0'}, 'JobName': {0: 'newt_d4snw51x'}, 'AveDiskWrite': {0: ''}, 'MaxDiskReadTask': {0: ''}, 'ConsumedEnergy': {0: ''}, 'AveRSS': {0: ''}, 'AveCPUFreq': {0: ''}, 'MaxDiskWrite': {0: ''}, 'AveVMSize': {0: ''}, 'MaxVMSizeNode': {0: ''}, 'MaxRSSTask': {0: ''}, 'MaxRSSNode': {0: ''}, 'MaxPagesTask': {0: ''}, 'NTasks': {0: ''}, 'MaxDiskWriteTask': {0: ''}, 'State': {0: 'PENDING'}, 'ReqCPUFreq': {0: ''}, 'MaxRSS': {0: ''}, 'MaxPagesNode': {0: ''}}}
output = json.dumps(wrapper)
print(output)

