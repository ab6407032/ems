from datetime import datetime, time, timedelta
import re
import gzip
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import pytz

# Function to read the gzipped XML file line by line
def read_gz_file(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            yield line

# Function to read the XML file line by line
def read_xml_file(file_path):
    # Example implementation: read lines from a file
    with open(file_path, 'r') as file:
        for line in file:
            yield line

# Function to find or create a counter in the result list
def get_or_create_counter(result, counter):
    for item in result:
        if counter in item:
            return item[counter]
    new_entry = {counter: []}
    result.append(new_entry)
    return new_entry[counter]

def extract_details(filename):
    print(filename)
    # Extract the date and time portion
    date_time_part = re.search(r"A(\d{8})\.(\d{4}-\d{4}-\d{4}-\d{4})", filename)

    # Extract the node name (MeContext)
    node_name_part = re.search(r"MeContext=([A-Za-z0-9_]+)", filename)

    # Format the date and extract the time
    date_str = date_time_part.group(1)
    time_str = date_time_part.group(2)
    formatted_date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
    time_range = time_str.split('-')

    # Extract the node name
    node_name = node_name_part.group(1) if node_name_part else "Unknown"

    return formatted_date, time_range, node_name

# Function to extract counters and their respective values
def extract_counters_and_values(file_path):
    result = []
    current_counters = []
    current_values = []
    timing_data = {
        "start_time": "",
        "time_zone_offset_start": "",
        "duration": ""
    }
    node = ""

    for line in read_xml_file(file_path):
        line = line.strip()

        if line == "<mi>":
            current_counters = []
            current_values = []
        elif line.startswith("<mt>") and line.endswith("</mt>"):
            current_counters.append(line[4:-5])
        elif line == "<mv>":
            temp_values = []
        elif line.startswith("<r>") and line.endswith("</r>"):
            val = line[3:-4]
            if bool(re.match(r'^\d+(\.\d+)?$', val)):
              val = float(val)
            temp_values.append(val)
        elif line == "</mv>":
            current_values.append(temp_values)
        elif line == "</mi>":
            for i, counter in enumerate(current_counters):
                counter_values = [v[i] for v in current_values if len(v) > i]
                existing_values = get_or_create_counter(result, counter)
                existing_values.extend(counter_values)
        elif line.startswith("<mts>") and line.endswith("</mts>"):
            if timing_data['start_time'] == "":
                timing_data['start_time'] = line[5:-6] 
        elif line.startswith("<cbt>") and line.endswith("</cbt>"):  # This could be the collection base time or similar
            if timing_data['time_zone_offset_start'] == "":
                timing_data['time_zone_offset_start'] = line[5:-6] 
        elif line.startswith("<gp>") and line.endswith("</gp>"): # Assuming this is a duration or gap, could relate to end time
            if timing_data['duration'] == "":
                timing_data['duration'] = line[4:-5]
        elif line.startswith("<neun>") and line.endswith("</neun>"):
            #<neun>JMCARNC01</neun>
            if node == "":
                node = line[6:-7] 


    return result, timing_data, node
    
def load_file_contents_db():
    from monitor.models import NodeLogFile, NodeMetric
    # Let's start by reading the contents of the uploaded file to understand its structure and content
    files = NodeLogFile.objects.filter(processed = False)

    for item in files:
        file_path = item.file.path


        # Parse metrics from each section and store them in a list
        extracted_data, timing_data, node = extract_counters_and_values(file_path)

        metrics = {
            "iub_throughput_utilization": calc_iub_throughput_utilization(extracted_data),
            "voice_traffic": calc_voice_traffic(extracted_data),
            "nas_success_rate_cs" : calc_nas_success_rate_cs(extracted_data),
            "rrc_success_rate_cs": calc_rrc_success_rate_cs(extracted_data),
            "rrc_success_rate_ps": calc_rrc_success_rate_ps(extracted_data),
            "hs_drop": calc_hs_drop(extracted_data),
            "csfb_success_rate": calc_csfb_success_rate(extracted_data)

        }

        start_time_dt = datetime.strptime(timing_data['start_time'], "%Y%m%d%H%M%SZ").replace(tzinfo=pytz.UTC)

        # Calculate end time by adding the duration
        duration_seconds = int(timing_data['duration'])
        end_time_dt = start_time_dt + timedelta(seconds=duration_seconds)

        # Formatting the start and end times for Django DateTimeField compatibility
        formatted_start_time = start_time_dt.strftime("%Y-%m-%d %H:%M:%S%z")
        formatted_end_time = end_time_dt.strftime("%Y-%m-%d %H:%M:%S%z")
        print(metrics, node, formatted_start_time, formatted_end_time)
        
        parsed_data = []
        # Loop through the dictionary
        for metric_name, metric_value in metrics.items():
            parsed_data.append(
                            NodeMetric(
                                node = item.node,
                                logfile = item,
                                metric = metric_name,
                                value = metric_value,
                            )
                        )
        
        NodeMetric.objects.bulk_create(parsed_data)
        item.processed = True
        item.metric_calculation = True
        item.start_time = formatted_start_time
        item.end_time = formatted_end_time
        item.save()

        print(metrics)
    

def calc_iub_throughput_utilization(extracted_data):
    pmSumCapacity = sum(get_or_create_counter(extracted_data, 'pmSumCapacity'))
    pmSamplesCapacity = sum(get_or_create_counter(extracted_data, 'pmSamplesCapacity'))
    pmCapacityLimit = sum(get_or_create_counter(extracted_data, 'pmCapacityLimit'))
    iub_throughput_utilization = (100 * (pmSumCapacity / pmSamplesCapacity)) / pmCapacityLimit
    return iub_throughput_utilization
    

def calc_voice_traffic(extracted_data):
    pmSumBestCs12Establish = sum(get_or_create_counter(extracted_data, 'pmSumBestCs12Establish'))
    pmSumBestAmr12200RabEstablish = sum(get_or_create_counter(extracted_data, 'pmSumBestAmr12200RabEstablish'))
    pmSumBestAmr7950RabEstablish = sum(get_or_create_counter(extracted_data, 'pmSumBestAmr7950RabEstablish'))
    pmSumBestAmr5900RabEstablish = sum(get_or_create_counter(extracted_data, 'pmSumBestAmr5900RabEstablish'))
    pmSumBestAmr4750RabEstablish = sum(get_or_create_counter(extracted_data, 'pmSumBestAmr4750RabEstablish'))
    pmSumBestAmrWbRabEstablish = sum(get_or_create_counter(extracted_data, 'pmSumBestAmrWbRabEstablish'))
    pmSumBestAmrNbMmRabEstablish = sum(get_or_create_counter(extracted_data, 'pmSumBestAmrNbMmRabEstablish'))
    voice_traffic = (pmSumBestCs12Establish + pmSumBestAmr12200RabEstablish + pmSumBestAmr7950RabEstablish + pmSumBestAmr5900RabEstablish + pmSumBestAmr4750RabEstablish + pmSumBestAmrWbRabEstablish + pmSumBestAmrNbMmRabEstablish) / 180
    return voice_traffic
    

def calc_nas_success_rate_cs(extracted_data):
    pmNoNormalNasSignReleaseCs = sum(get_or_create_counter(extracted_data, 'pmNoNormalNasSignReleaseCs'))
    pmNoSystemNasSignReleaseCs = sum(get_or_create_counter(extracted_data, 'pmNoSystemNasSignReleaseCs'))
    nas_success_rate_cs = 100 * (pmNoNormalNasSignReleaseCs / (pmNoNormalNasSignReleaseCs + pmNoSystemNasSignReleaseCs))
    return nas_success_rate_cs
    

def calc_rrc_success_rate_cs(extracted_data):
    pmTotNoRrcConnectReqCsSucc = sum(get_or_create_counter(extracted_data, 'pmTotNoRrcConnectReqCsSucc'))
    pmTotNoRrcConnectReqCs = sum(get_or_create_counter(extracted_data, 'pmTotNoRrcConnectReqCs'))
    pmNoLoadSharingRrcConnCs = sum(get_or_create_counter(extracted_data, 'pmNoLoadSharingRrcConnCs'))
    #pmNoLoadSharingRrcConnCs
    rrc_success_rate_cs = 100 * (pmTotNoRrcConnectReqCsSucc / (pmTotNoRrcConnectReqCs - pmNoLoadSharingRrcConnCs))
    return rrc_success_rate_cs
    

def calc_rrc_success_rate_ps(extracted_data):
    pmTotNoRrcConnectReqPsSucc = sum(get_or_create_counter(extracted_data, 'pmTotNoRrcConnectReqPsSucc'))
    pmTotNoRrcConnectReqPs = sum(get_or_create_counter(extracted_data, 'pmTotNoRrcConnectReqPs'))
    pmNoLoadSharingRrcConnPs = sum(get_or_create_counter(extracted_data, 'pmNoLoadSharingRrcConnPs'))
    # pmNoLoadSharingRrcConnPs
    rrc_success_rate_ps = 100 * (pmTotNoRrcConnectReqPsSucc / (pmTotNoRrcConnectReqPs - pmNoLoadSharingRrcConnPs))
    return rrc_success_rate_ps

def calc_hs_drop(extracted_data):
    pmNoSystemRbReleaseHs = sum(get_or_create_counter(extracted_data, 'pmNoSystemRbReleaseHs'))
    pmChSwitchAttemptHsUra = sum(get_or_create_counter(extracted_data, 'pmChSwitchAttemptHsUra'))
    pmChSwitchSuccHsUra = sum(get_or_create_counter(extracted_data, 'pmChSwitchSuccHsUra'))
    pmNoNormalRbReleaseHs = sum(get_or_create_counter(extracted_data, 'pmNoNormalRbReleaseHs'))
    pmNoSuccRbReconfPsIntDch = sum(get_or_create_counter(extracted_data, 'pmNoSuccRbReconfPsIntDch'))
    pmPsIntHsToFachSucc = sum(get_or_create_counter(extracted_data, 'pmPsIntHsToFachSucc'))
    hs_drop = 100 * ((pmNoSystemRbReleaseHs - pmChSwitchAttemptHsUra + pmChSwitchSuccHsUra) / (pmNoSystemRbReleaseHs + pmNoNormalRbReleaseHs + pmNoSuccRbReconfPsIntDch + pmPsIntHsToFachSucc + pmChSwitchSuccHsUra))
    return hs_drop

def calc_csfb_success_rate(extracted_data):
    pmTotNoRrcConnReqCsfbIndSucc = sum(get_or_create_counter(extracted_data, 'pmTotNoRrcConnReqCsfbIndSucc'))
    pmTotNoRrcConnReqCsfbInd = sum(get_or_create_counter(extracted_data, 'pmTotNoRrcConnReqCsfbInd'))
    pmNoNormalNasSignRelCsfbInd = sum(get_or_create_counter(extracted_data, 'pmNoNormalNasSignRelCsfbInd'))
    pmNoSystemNasSignRelCsfbInd = sum(get_or_create_counter(extracted_data, 'pmNoSystemNasSignRelCsfbInd'))
    pmNoRabEstSuccCsfbInd = sum(get_or_create_counter(extracted_data, 'pmNoRabEstSuccCsfbInd'))
    pmNoRabEstSuccCsfbDetect = sum(get_or_create_counter(extracted_data, 'pmNoRabEstSuccCsfbDetect'))
    pmNoRabEstAttCsfbInd = sum(get_or_create_counter(extracted_data, 'pmNoRabEstAttCsfbInd'))
    pmNoRabEstAttCsfbDetect = sum(get_or_create_counter(extracted_data, 'pmNoRabEstAttCsfbDetect'))
    csfb_success_rate = 100 * (( pmTotNoRrcConnReqCsfbIndSucc / pmTotNoRrcConnReqCsfbInd ) * ( pmNoNormalNasSignRelCsfbInd / ( pmNoNormalNasSignRelCsfbInd + pmNoSystemNasSignRelCsfbInd )) * (( pmNoRabEstSuccCsfbInd + pmNoRabEstSuccCsfbDetect) / (pmNoRabEstAttCsfbInd + pmNoRabEstAttCsfbDetect)))
    return csfb_success_rate