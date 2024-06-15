#include "Flash_Zone_Manager_Base.h"


namespace SSD_Components
{
	Flash_Zone_Manager_Base::Flash_Zone_Manager_Base(unsigned int channel_count, unsigned int chip_no_per_channel, 
							unsigned int die_no_per_chip, unsigned int plane_no_per_die,
							unsigned int block_no_per_plane, unsigned int page_no_per_block,
							unsigned int page_capacity, unsigned int zone_size, 
							unsigned int channel_no_per_zone, unsigned int chip_no_per_zone, unsigned int die_no_per_zone, unsigned int plane_no_per_zone) : channel_count(channel_count), chip_no_per_channel(chip_no_per_channel), die_no_per_chip(die_no_per_chip), plane_no_per_die(plane_no_per_die), block_no_per_plane(block_no_per_plane), pages_no_per_block(page_no_per_block), page_capacity(page_capacity), zone_size(zone_size), Channel_no_per_zone(channel_no_per_zone), Chip_no_per_zone(chip_no_per_zone), Die_no_per_zone(die_no_per_zone), Plane_no_per_zone(plane_no_per_zone)
	{
		unsigned int device_size = channel_count * chip_no_per_channel * die_no_per_chip * plane_no_per_die * block_no_per_plane / 1024 * pages_no_per_block / 1024 * page_capacity;

		zone_count = device_size / zone_size;

		zones = new NVM::FlashMemory::Zone*[zone_count];

		for (unsigned int ZoneID = 0; ZoneID < zone_count; ZoneID++)
		{
			zones[ZoneID] = new NVM::FlashMemory::Zone(ZoneID, channel_count, 
								chip_no_per_channel, die_no_per_chip, plane_no_per_die);
		}
	}

	Flash_Zone_Manager_Base::~Flash_Zone_Manager_Base()
	{
		delete[] zones;
	}

	void Flash_Zone_Manager_Base::open_zone(unsigned int zone_id)
	{
		// put a zone id in the begining of the open_zones list
		// if the zone is already in the list, bring it to the front of the list, the least recently used zone is at the end of the list and will be remove from the list
		// if it's not in it, then add it to the front of the list and remove the least recently used zone from the list

		for (unsigned int i = 0; i < max_open_zone; i++)
		{
			if (open_zones[i] == zone_id)
			{
				for (unsigned int j = i; j > 0; j--)
				{
					open_zones[j] = open_zones[j - 1];
				}
				open_zones[0] = zone_id;
				return;
			}
		}
		for (unsigned int i = max_open_zone - 1; i > 0; i--)
		{
			open_zones[i] = open_zones[i - 1];
		}
		open_zones[0] = zone_id;
		Stats::Zone_Opened_Count++;
	}
}
