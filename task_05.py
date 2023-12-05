from task import Task


class Task05(Task):

    def part_one(self) -> int:
        seed_input, *mappings_input = self.input.split('\n\n')

        seeds = map(int, seed_input.split(':')[1].split())
        mappings = self._mappings(mappings_input)

        sources = seeds
        destinations = []

        for mapping in mappings:
            destinations = []

            for source in sources:
                for map_dest_start, map_source_start, map_size in mapping:
                    if map_source_start <= source < map_source_start + map_size:
                        destinations.append(source - map_source_start + map_dest_start)

                        break
                else:
                    destinations.append(source)

            sources = destinations

        return min(destinations)

    def part_two(self) -> int:
        seed_input, *mappings_input = self.input.split('\n\n')

        seeds = list(map(int, seed_input.split(':')[1].split()))
        seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
        mappings = self._mappings(mappings_input)

        sources = seed_ranges
        destinations = []

        for mapping in mappings:
            destinations = []

            for source_start, source_end in sources:
                for map_dest_start, map_source_start, map_size in mapping:
                    overlap_start = max(source_start, map_source_start)
                    overlap_end = min(source_end, map_source_start + map_size)

                    if overlap_start < overlap_end:
                        destinations.append((overlap_start - map_source_start + map_dest_start, overlap_end - map_source_start + map_dest_start))

                        if overlap_start > source_start:
                            sources.append((source_start, overlap_start))

                        if source_end > overlap_end:
                            sources.append((overlap_end, source_end))

                        break
                else:
                    destinations.append((source_start, source_end))

            sources = destinations

        return min(destinations)[0]

    @staticmethod
    def _mappings(mappings_input) -> list[list[list[int]]]:
        return [[list(map(int, mapping.split())) for mapping in mapping_input.splitlines()[1:]] for mapping_input in mappings_input]
