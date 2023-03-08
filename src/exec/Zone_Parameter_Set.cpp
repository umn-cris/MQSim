#include <algorithm>
#include <string.h>
#include "../sim/Engine.h"
#include "Zone_Parameter_Set.h"

unsigned int Zone_Parameter_Set::Zone_Size = 256; // Zone size in MB
unsigned int Zone_Parameter_Set::Channel_No_Per_Zone = 8;
unsigned int Zone_Parameter_Set::Chip_No_Per_Zone = 2;
unsigned int Zone_Parameter_Set::Die_No_Per_Zone = 2;
unsigned int Zone_Parameter_Set::Plane_No_Per_Zone = 2;



void Zone_Parameter_Set::XML_serialize(Utils::XmlWriter& xmlwriter)
{
	std::string tmp;
	tmp = "Zone_Parameter_Set";
	xmlwriter.Write_open_tag(tmp);

	std::string attr = "Zone_Size";
	std::string val = std::to_string(Zone_Size);
	xmlwriter.Write_attribute_string(attr, val);

	attr = "Channel_No_Per_Zone";
	val = std::to_string(Channel_No_Per_Zone);
	xmlwriter.Write_attribute_string(attr, val);

	attr = "Chip_No_Per_Zone";
	val = std::to_string(Chip_No_Per_Zone);
	xmlwriter.Write_attribute_string(attr, val);

	attr = "Die_No_Per_Zone";
	val = std::to_string(Die_No_Per_Zone);
	xmlwriter.Write_attribute_string(attr, val);

	attr = "Plane_No_Per_Zone";
	val = std::to_string(Plane_No_Per_Zone);
	xmlwriter.Write_attribute_string(attr, val);

	attr = "Zone_Allocation_Scheme";
	switch (Zone_allocation_scheme) {
	 	case SSD_Components::Zone_Allocation_Scheme_Type::CDPW:
			val = "CDPW";
			break;
		 default:
	 		break;
	}
	xmlwriter.Write_attribute_string(attr, val);

	attr = "SubZone_Allocation_Scheme";
	switch (SubZone_allocation_scheme) {
		case SSD_Components::SubZone_Allocation_Scheme_Type::CDPW:
			val = "CDPW";
			break;	
		default:
	 		break;
	}
	xmlwriter.Write_attribute_string(attr, val);

	xmlwriter.Write_close_tag();
}

void Zone_Parameter_Set::XML_deserialize(rapidxml::xml_node<> *node)
{
	try {
		for (auto param = node->first_node(); param; param = param->next_sibling()) {
			if (strcmp(param->name(), "Zone_Size") == 0) {
				std::string val = param->value();
				Zone_Size = std::stoull(val);
			} else if (strcmp(param->name(), "Channel_No_Per_Zone") == 0) {
				std::string val = param->value();
				Channel_No_Per_Zone = std::stoull(val);
			} else if (strcmp(param->name(), "Chip_No_Per_Zone") == 0) {
				std::string val = param->value();
				Chip_No_Per_Zone = std::stoull(val);
			} else if (strcmp(param->name(), "Die_No_Per_Zone") == 0) {
				std::string val = param->value();
				Die_No_Per_Zone = std::stoull(val);	
			} else if (strcmp(param->name(), "Plane_No_Per_Zone") == 0) {
				std::string val = param->value();
				Plane_No_Per_Zone = std::stoull(val);
			} else if (strcmp(param->name(), "Zone_Allocation_Scheme") == 0) {
			 	std::string val = param->value();
			 	std::transform(val.begin(), val.end(), val.begin(), ::toupper);
			 	if (strcmp(val.c_str(), "CDPW") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::CDPW;
			 	} else if (strcmp(val.c_str(), "CDWP") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::CDWP;
				} else if (strcmp(val.c_str(), "CPDW") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::CPDW;
				} else if (strcmp(val.c_str(), "CPWD") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::CPWD;
				} else if (strcmp(val.c_str(), "CWDP") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::CWDP;
				} else if (strcmp(val.c_str(), "CWPD") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::CWPD;
			 	} else if (strcmp(val.c_str(), "DCPW") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::DCPW;
				} else if (strcmp(val.c_str(), "DCWP") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::DCWP;
			 	} else if (strcmp(val.c_str(), "DPCW") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::DPCW;
				} else if (strcmp(val.c_str(), "DPWC") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::DPWC;
				} else if (strcmp(val.c_str(), "DWCP") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::DWCP;
				} else if (strcmp(val.c_str(), "DWPC") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::DWPC;
			 	} else if (strcmp(val.c_str(), "PCDW") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::PCDW;
				} else if (strcmp(val.c_str(), "PCWD") == 0) {
					Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::PCWD;
				} else if (strcmp(val.c_str(), "PDCW") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::PDCW;
				} else if (strcmp(val.c_str(), "PDWC") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::PDWC;
				} else if (strcmp(val.c_str(), "PWCD") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::PWCD;
				} else if (strcmp(val.c_str(), "PWDC") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::PWDC;
			 	} else if (strcmp(val.c_str(), "WCDP") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::WCDP;
				} else if (strcmp(val.c_str(), "WCPD") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::WCPD;
				} else if (strcmp(val.c_str(), "WDCP") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::WDCP;
				} else if (strcmp(val.c_str(), "WDPC") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::WDPC;
				} else if (strcmp(val.c_str(), "WPCD") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::WPCD;
				} else if (strcmp(val.c_str(), "WPDC") == 0) {
			 		Zone_allocation_scheme = SSD_Components::Zone_Allocation_Scheme_Type::WPDC;
				} else {
					PRINT_ERROR("Unknown Zone_Allocation_Scheme type specified in the input file.")
				}
			 } else if (strcmp(param->name(), "SubZone_Allocation_Scheme") == 0) {
			 	std::string val = param->value();
			 	std::transform(val.begin(), val.end(), val.begin(), ::toupper);
			 	if (strcmp(val.c_str(), "CDPW") == 0) {
					 SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::CDPW;
			 	} else if (strcmp(val.c_str(), "CDWP") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::CDWP;
				} else if (strcmp(val.c_str(), "CPDW") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::CPDW;
				} else if (strcmp(val.c_str(), "CPWD") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::CPWD;
				} else if (strcmp(val.c_str(), "CWDP") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::CWDP;
				} else if (strcmp(val.c_str(), "CWPD") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::CWPD;
			 	} else if (strcmp(val.c_str(), "DCPW") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::DCPW;
				} else if (strcmp(val.c_str(), "DCWP") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::DCWP;
			 	} else if (strcmp(val.c_str(), "DPCW") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::DPCW;
				} else if (strcmp(val.c_str(), "DPWC") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::DPWC;
				} else if (strcmp(val.c_str(), "DWCP") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::DWCP;
				} else if (strcmp(val.c_str(), "DWPC") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::DWPC;
			 	} else if (strcmp(val.c_str(), "PCDW") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::PCDW;
				} else if (strcmp(val.c_str(), "PCWD") == 0) {
					SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::PCWD;
				} else if (strcmp(val.c_str(), "PDCW") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::PDCW;
				} else if (strcmp(val.c_str(), "PDWC") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::PDWC;
				} else if (strcmp(val.c_str(), "PWCD") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::PWCD;
				} else if (strcmp(val.c_str(), "PWDC") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::PWDC;
			 	} else if (strcmp(val.c_str(), "WCDP") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::WCDP;
				} else if (strcmp(val.c_str(), "WCPD") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::WCPD;
				} else if (strcmp(val.c_str(), "WDCP") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::WDCP;
				} else if (strcmp(val.c_str(), "WDPC") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::WDPC;
				} else if (strcmp(val.c_str(), "WPCD") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::WPCD;
				} else if (strcmp(val.c_str(), "WPDC") == 0) {
			 		SubZone_allocation_scheme = SSD_Components::SubZone_Allocation_Scheme_Type::WPDC;
				} else {
					PRINT_ERROR("Unknown SubZone_Allocation_Scheme specified in the input file")
				}
			 }
		}
	} catch (...) {
		PRINT_ERROR("Error in the Flash_Parameter_Set!")
	}
}
