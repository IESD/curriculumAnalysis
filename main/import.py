from pathlib import Path

def extractData(path, split_string):
    with path.open('r', encoding='utf8') as f:
        data = f.read();
        chunks = data.split(split_string)
        chunks = [ch.splitlines() for ch in chunks]
        # chunks = [[line.strip() for line in ch if line.strip()] for ch in chunks]
        chunks[0] = ['deleteme', '', *chunks[0]]
        chunks = [ch[1:] for ch in chunks][:-1]
        for chunk in chunks:
            yield chunk

def extractProgrammes(path):
    for chunk in extractData(path, 'End of Programme Specification for'):
        yield(Programme(chunk))

def extractModules(path):
    for chunk in extractData(path, 'End of Programme Specification for'):
        yield(Programme(chunk))


def aggregate_until(data, end_item):
    result = []
    while True:
        if data[0].startswith(end_item):
            break
        row = data.pop(0).strip()
        if not row:
            continue
        result.append(row)
    return result

class Module:
    def __init__(self, data):
        assert data[3] == "Module Specification"
        assert data[9] == "Module Full Title: "
        assert data[15] == "Module Short Title: "
        assert data[17] == "Module Code: "
        assert data[19] == "Credit Value: "
        assert data[23] == "Credit Level: "
        assert data[29] == "Faculty: "
        assert data[33] == "School: "
        assert data[37] == "Department: "
        assert data[41] == "Module Leader: "
        assert data[45] == "Module Appraiser(s) / Marker(s): "

        self.full_name = data[11]
        self.short_name = data[13]
        self.credit_value = data[21]
        self.credit_level = data[25]
        self.code = data[27]
        self.faculty = data[31]
        self.school = data[35]
        self.department = data[39]
        self.module_leader = data[43]
        data = data[46:]

        self.module_appraisers = aggregate_until(data, "Offered at the following sites:")
        assert data[0] == "Offered at the following sites:"
        data = data[1:]

        self.sites = aggregate_until(data, "Semester / Year-long:")
        assert data[0] == "Semester / Year-long: "
        data = data[1:]

        self.intakes = aggregate_until(data, "DMUGlobal Content indicator:")

        assert data[0] == "DMUGlobal Content indicator: "
        assert data[2] in ["Y", "N"]
        self.DMUGlobal = data[2] == "Y"

        assert data[4] == "Ethical approval required: "
        assert data[6] in ["Y", "N"]
        self.ethical_approval = data[6] == "Y"


        assert data[8] == "Details of Accreditation by Professional, Statutory or Regulatory Body:"
        data = data[9:]
        self.accreditation = aggregate_until(data, "Module Pre-requisites:")
        assert data[0] == "Module Pre-requisites:"
        data = data[1:]

        # self.accreditation = aggregate_until(data, "Module Pre-requisites:")
        # assert data[0] == "Module Pre-requisites:"
        # data = data[1:]

        self.prerequisites = aggregate_until(data, "Module Description:")
        assert data[0] == "Module Description:"
        assert data[3] == "Learning Outcomes:"

        self.description = data[1]
        self.learning_outcomes = data[4]
        # if self.prerequisites: print(self.prerequisites)

        assert data[6].strip() == "Evaluation:"

        assessment_keys = data[7].split('\t')
        data = data[8:]
        assert len(assessment_keys) == 8
        assessments = aggregate_until(data, "Anonymous marking exemption codes:")
        self.assessments = [{k: v for k, v in zip(assessment_keys, a.split('\t'))} for a in assessments]
        assert data[0] == "Anonymous marking exemption codes: OPTO1: Individually distinct work; OPTO2: Reflection on development of own work; OPTO3:"

        assert data[3] == "Assessment Notes:" 
        self.assessment_notes = data[4]

        assert data[6] == "Reassessment:" 
        self.reassessment = data[7]

        assert data[9] == "Expected Methods of Delivery:" 
        self.method_of_delivery = data[10]

        assert data[12].strip() == "Programmes using this module:"
        programme_keys = data[15].split('\t')
        data = data[16:]
        programmes = aggregate_until(data, "Remarks:")
        self.programmes = [{k: v for k, v in zip(programme_keys, p.split('\t'))} for p in programmes]
        assert data == ["Remarks:", "", ""]

    def corpus(self):
        """
        This method should return the main corpus for this module.
        Make adjustments here to control what we actually analyse.
        """
        return {
            self.description
        }

class Programme:
    def __init__(self, data):
        self.data = data

root = Path(__file__).parent.parent / "import"
m = root / "0324_Module_Specification_for_Academics.txt"
p = root / "0325_Programme_Specification_for_Academics.txt"
modules = [Module(ch) for ch in extractData(m, 'End of Module Specification for')]
programmes = [Programme(ch) for ch in extractData(p, 'End of Programme Specification for')]
