import requests as req

def fetch_courses(subj_area, div):
    BASE = 'https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?'
    return req.get(BASE, params={'SA': subj_area, 'funsel': '3'})

def fetch_root_sections(course, options, term):
    default_filters = '{"enrollment_status":"O,W,C,X,T,S","advanced":"y","meet_days":"M,T,W,R,F","start_time":"8:00 am","end_time":"8:00 pm","meet_locations":null,"meet_units":null,"instructor":null,"class_career":null,"impacted":null,"enrollment_restrictions":null,"enforced_requisites":null,"individual_studies":null,"summer_session":null}'
    BASE = 'https://sa.ucla.edu/ro/Public/SOC/Results/GetCourseSummary?'
    return req.get(BASE, params={'model': course.to_jsons(term), 'FilterFlags': default_filters})

def fetch_leaf_sections(section, options, term):
    default_filters = '{"enrollment_status":"O,W,C,X,T,S","advanced":"y","meet_days":"M,T,W,R,F","start_time":"8:00 am","end_time":"8:00 pm","meet_locations":null,"meet_units":null,"instructor":null,"class_career":null,"impacted":null,"enrollment_restrictions":null,"enforced_requisites":null,"individual_studies":null,"summer_session":null}'
    BASE = 'https://sa.ucla.edu/ro/Public/SOC/Results/GetCourseSummary?'
    return req.get(BASE, params={'model': section.to_jsons(), 'FilterFlags': default_filters})

def fetch_section_detail(section):
    BASE = 'https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetailTooltip?'
    query = {
        'term_cd': section.term, 
        'subj_area_cd': section.course.subj_area, 
        'crs_catlg_no': section.course.get_padded_ctlg_no(), 
        'class_id': section.id,
        'class_no': section.sec_no
        }
    # We need to spoof a X-Requested-With header or else the response will just be a generic "Not found" page
    return req.get(BASE, params=query, headers={'X-Requested-With': 'XMLHttpRequest'})
