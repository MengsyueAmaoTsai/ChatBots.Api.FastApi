from typing import Optional

from assertpy import assert_that

from configuration import ConfigurationBuilder, MemoryConfigurationSource


class ConfigurationTests:
    def test_load_and_combine_key_value_pairs_from_different_configuration_providers(self) -> None:
        # Arrange
        dict_1: dict[str, Optional[str]] = {
            "Mem1:KeyInMem1": "ValueInMem1",
        }

        dict_2: dict[str, Optional[str]] = {
            "Mem2:KeyInMem2": "ValueInMem2",
        }

        dict_3: dict[str, Optional[str]] = {
            "Mem3:KeyInMem3": "ValueInMem3",
        }

        mem_config_src_1 = MemoryConfigurationSource(initial_data=dict_1)
        mem_config_src_2 = MemoryConfigurationSource(initial_data=dict_2)
        mem_config_src_3 = MemoryConfigurationSource(initial_data=dict_3)

        builder = ConfigurationBuilder()

        # Act
        builder.add(mem_config_src_1)
        builder.add(mem_config_src_2)
        builder.add(mem_config_src_3)

        config = builder.build()

        mem_value_1 = config["Mem1:KeyInMem1"]
        mem_value_2 = config["Mem2:KeyInMem2"]
        mem_value_3 = config["Mem3:KeyInMem3"]

        # Assert
        assert_that(builder.sources).contains(mem_config_src_1, mem_config_src_2, mem_config_src_3)
        assert_that(mem_value_1).is_equal_to("ValueInMem1")
        assert_that(mem_value_2).is_equal_to("ValueInMem2")
        assert_that(mem_value_3).is_equal_to("ValueInMem3")
        assert_that(mem_value_1).is_equal_to(config["Mem1:KeyInMem1"])
        assert_that(mem_value_2).is_equal_to(config["Mem2:KeyInMem2"])
        assert_that(mem_value_3).is_equal_to(config["Mem3:KeyInMem3"])
        assert_that(config["NotExistingKey"]).is_none()
