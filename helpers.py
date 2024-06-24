from datetime import datetime, time
import re
from monitor.models import RouterLogFile, RouterLog, RouterLogScore
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time
    
def load_file_contents_db():
    # Let's start by reading the contents of the uploaded file to understand its structure and content
    files = RouterLogFile.objects.filter(processed = False)

    for item in files:
        file_path = item.file.path

        with open(file_path, 'r') as file:
            log_content = file.readlines()
        
        # Extract sections from the log content
        sections = extract_sections(log_content)

        # Parse metrics from each section and store them in a list
        parsed_data = []

        for section in sections:
            timestamp, keyword, keyword_no, metrics = parse_metrics(section)
            for metric in metrics:
                if(keyword is not None):
                    # print(metric)
                    if(metric[1] > 0):
                        parsed_data.append(
                            RouterLog(
                                logfile=item,
                                timestamp=timestamp, 
                                keyword=keyword, 
                                keyword_no=keyword_no,
                                counter_no=metric[0],
                                counter_name=metric[2],
                                counter_value=metric[1],
                                )
                        )

        RouterLog.objects.bulk_create(parsed_data)
        item.processed = True
        item.save()
    # return parsed_data
    

    # Function to extract sections based on timestamps
def extract_sections(log_content):
    sections = []
    current_section = []

    for line in log_content:
        if re.match(r'^\w{3} \w{3} \d{2}, \d{2}:\d{2}', line):  # Match lines with date and time
            if current_section:
                sections.append(current_section)
                current_section = []
        current_section.append(line)
    if current_section:  # Append the last section
        sections.append(current_section)

    return sections

# Function to parse metrics from a section
def parse_metrics(section):
    timestamp = None
    keyword = None
    keyword_no = None
    metrics = []

    for line in section:
        if re.match(r'^\w{3} \w{3} \d{2}, \d{2}:\d{2}', line):
            timestamp = line.strip()
            timestamp = timestamp.replace("(OK)", "").strip()
            timestamp = "{} {}".format(timestamp[:-14], timestamp[-10:])
            datetime_format = "%a %b %d, %H:%M %z %Y"
            timestamp = datetime.strptime(timestamp, datetime_format)
        #elif line.startswith("CLTCH:") or line.startswith("CELTCHF:") or line.startswith("CELTCHH:") or line.startswith("CLSDCCH:") or line.startswith("NICELASS:") or line.startswith("NECELASS:") or line.startswith("NCELLREL:"):
        elif line.startswith("CELTCHF:") or line.startswith("CELTCHH:") or line.startswith("CLSDCCH:"):
            keyword = line.split(": '")[0]
            keyword_no = line.split("'")[1]
        elif re.match(r'^\s*\d+', line):
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) == 3:
                metrics.append((int(parts[0]), int(parts[1]), parts[2]))

    return timestamp, keyword, keyword_no, metrics


#load_file_contents_db()

def calculate_scores():
    files = RouterLogFile.objects.filter(processed = True)

    for item in files:
        queryset = RouterLog.objects.filter(logfile = item).values_list(
            'keyword', 'counter_name', 'counter_value'
        )
        df = pd.DataFrame(list(queryset), columns=['keyword', 'counter_name', 'counter_value'])
        #print(df)
        # return
        dfTrafficVoice = df[
            (
                (df['keyword']=='CELTCHF') | (df['keyword']=='CELTCHH')
            ) & 
            (
                (df['counter_name']=='TFTRALACC') | (df['counter_name']=='THTRALACC')
            )
        ]
        #print(dfTrafficVoice)
        traffic_voice_2g = dfTrafficVoice['counter_value'].sum() / 360
        
        # traffic_voice_2g = Decimal(f"{traffic_voice_2g:.2f}").quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        #print(traffic_voice_2g)
        dfTCHDrop_1 = df[
            (
                (df['keyword']=='CELTCHF') | (df['keyword']=='CELTCHH')
            ) & 
            (
                (df['counter_name']=='TFNDROP') | (df['counter_name']=='THNDROP') | (df['counter_name']=='TFNDROPSUB') | (df['counter_name']=='THNDROPSUB')
            )
        ]
        tchdrop_1 = dfTCHDrop_1['counter_value'].sum()
        dfTCHDrop_2 = df[
            (
                (df['keyword']=='CELTCHF') | (df['keyword']=='CELTCHH')
            ) & 
            (
                (df['counter_name']=='TFCASSALL') | (df['counter_name']=='THCASSALL') | (df['counter_name']=='THCASSALLSUB') | (df['counter_name']=='TFCASSALLSUB')
            )
        ]
        tchdrop_2 = dfTCHDrop_2['counter_value'].sum()
        tchdrop = 0.0
        if(tchdrop_2 > 0):
            tchdrop = 100 * (tchdrop_1 / tchdrop_2)
            # tchdrop = Decimal(f"{tchdrop:.2f}").quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        dfCNDrop = df[(df['keyword']=='CLSDCCH') & (df['counter_name']=='CNDROP')]
        cndrop = dfCNDrop['counter_value'].sum()
        dfCLUNDrop = df[(df['keyword']=='CLSDCCH') & (df['counter_name']=='CLUNDROP')]
        clunndrop = dfCLUNDrop['counter_value'].sum()
        dfCNRELCONG = df[(df['keyword']=='CLSDCCH') & (df['counter_name']=='CNRELCONG')]
        cnrelcong = dfCNRELCONG['counter_value'].sum()
        dfCMSESTAB = df[(df['keyword']=='CLSDCCH') & (df['counter_name']=='CMSESTAB')]
        cmsestab = dfCMSESTAB['counter_value'].sum()
        sdcch_drop = 0.0
        if(cmsestab > 0):
            sdcch_drop = 100 * ((cndrop - clunndrop - cnrelcong) / cmsestab)
            # sdcch_drop = Decimal(f"{sdcch_drop:.2f}").quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        



        # traffic_voice_2g = float(np.float64(traffic_voice_2g))
        # tchdrop = float(np.float64(tchdrop))
        # sdcch_drop = float(np.float64(sdcch_drop))
        item_score = RouterLogScore.objects.filter(logfile=item)
        print(traffic_voice_2g, tchdrop, sdcch_drop)
        if not item_score.exists():
            RouterLogScore.objects.create(
                traffic_voice_2g = traffic_voice_2g,
                tchdrop = tchdrop,
                sdcch_drop = sdcch_drop
            )
        else:
            
            item_1 = item_score.first()
            item_1.traffic_voice_2g = traffic_voice_2g
            item_1.tchdrop = tchdrop
            item_1.sdcch_drop = sdcch_drop
            item_1.save()
            
        item.traffic_voice_2g = traffic_voice_2g
        item.tchdrop = tchdrop
        item.sdcch_drop = sdcch_drop
        item.metric_calculation = True
        item.save()

#         >>> from monitor.models import RouterLog 
# >>> RouterLog.objects.all().delete()
