from assertpy import assert_that

from shared_kernel import Entity, SingleValueObject


class TestEntityId(SingleValueObject[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class TestEntity(Entity[TestEntityId]):
    def __init__(self, id: TestEntityId) -> None:
        super().__init__(id)


class EntityTests:
    def test_equals_when_entities_have_the_same_id_should_return_true(self) -> None:
        entity1 = TestEntity(TestEntityId("id"))
        entity2 = TestEntity(TestEntityId("id"))

        assert_that(entity1 == entity2).is_true()

    def test_equals_when_entities_have_different_ids_should_return_false(self) -> None:
        entity1 = TestEntity(TestEntityId("id"))
        entity2 = TestEntity(TestEntityId("different"))

        assert_that(entity1 == entity2).is_false()

    def test_get_hash_code_when_entities_have_the_same_id_should_return_the_same_hash_code(self) -> None:
        entity1 = TestEntity(TestEntityId("id"))
        entity2 = TestEntity(TestEntityId("id"))

        assert_that(hash(entity1)).is_equal_to(hash(entity2))

    def test_get_hash_code_when_entities_have_different_ids_should_return_different_hash_codes(self) -> None:
        entity1 = TestEntity(TestEntityId("id"))
        entity2 = TestEntity(TestEntityId("different"))

        assert_that(hash(entity1)).is_not_equal_to(hash(entity2))
