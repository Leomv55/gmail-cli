from unittest import TestCase

from gmail_cli.automate import AutomationSchemaValidation
from gmail_cli.exceptions import ValidationError


class TestAutomationValidationTestCase(TestCase):
    def setUp(self) -> None:
        self.validator_1 = AutomationSchemaValidation("samples/automate_1.json")

    def test_basic_rule_checks(self):
        self.assertEqual(self.validator_1.schema, self.validator_1.read_schema("samples/automate_1.json"))
        rule_1 = {
            "name": ""
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)
        rule_1 = {
            "name": "Rule 1",
            "description": ""
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)
        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "conditions": []
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)
        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "conditions": []
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)
        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "conditions": [],
            "actions": []
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)

        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "predicate": "all",
            "conditions": [{}],
            "actions": [{}]
        }
        self.assertDictEqual(self.validator_1._validate_rule(rule_1), rule_1)
        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "predicate": "any",
            "conditions": [{}],
            "actions": [{}]
        }
        self.assertDictEqual(self.validator_1._validate_rule(rule_1), rule_1)
        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "predicate": "invalid",
            "conditions": [{}],
            "actions": [{}]
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)

        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "predicate": "all",
            "conditions": "invalid",
            "actions": [{}]
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)
        rule_1 = {
            "name": "Rule 1",
            "description": "Description 1",
            "predicate": "all",
            "conditions": [{}],
            "actions": "invalid"
        }
        self.assertRaises(ValidationError, self.validator_1._validate_rule, rule_1)

    def test_basic_condition_checks(self):
        condition_1 = {
            "field": "",
            "predicate": "",
            "value": ""
        }
        self.assertRaises(ValidationError, self.validator_1._validate_condition, condition_1)
        condition_1 = {
            "field": "to",
            "operator": "",
            "value": ""
        }
        self.assertRaises(ValidationError, self.validator_1._validate_condition, condition_1)
        condition_1 = {
            "field": "to",
            "operator": "contains",
            "value": ""
        }
        self.assertRaises(ValidationError, self.validator_1._validate_condition, condition_1)
        condition_1 = {
            "field": "to",
            "operator": "contains",
            "value": "test"
        }
        self.assertDictEqual(self.validator_1._validate_condition(condition_1), condition_1)

    def test_condition_field_checks(self):
        condition_1 = {
            "field": "invalid",
            "operator": "contains",
            "value": "test"
        }
        self.assertRaises(ValidationError, self.validator_1.validate_condition, condition_1)
        condition_1 = {
            "field": "from",
            "operator": "contains",
            "value": "test"
        }
        self.assertDictEqual(self.validator_1.validate_condition(condition_1), condition_1)
        condition_1 = {
            "field": "to",
            "operator": "contains",
            "value": "test"
        }
        self.assertDictEqual(self.validator_1.validate_condition(condition_1), condition_1)
        condition_1 = {
            "field": "subject",
            "operator": "contains",
            "value": "test"
        }
        self.assertDictEqual(self.validator_1.validate_condition(condition_1), condition_1)
        condition_1 = {
            "field": "invalid",
            "operator": "contains",
            "value": "test"
        }
        self.assertRaises(ValidationError, self.validator_1.validate_condition, condition_1)
        condition_1 = {
            "field": "to",
            "operator": "invalid",
            "value": "test"
        }
        self.assertRaises(ValidationError, self.validator_1.validate_condition, condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "lt",
            "value": 2
        }
        self.assertDictEqual(self.validator_1.validate_condition(condition_1), condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "gt",
            "value": 2
        }
        self.assertDictEqual(self.validator_1.validate_condition(condition_1), condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "eq",
            "value": 2
        }
        self.assertRaises(ValidationError, self.validator_1.validate_condition, condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "neq",
            "value": 2
        }
        self.assertRaises(ValidationError, self.validator_1.validate_condition, condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "lt",
            "value": "test"
        }
        self.assertRaises(ValidationError, self.validator_1.validate_condition, condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "eq",
            "value": "12-12-2020"
        }
        self.assertDictEqual(self.validator_1.validate_condition(condition_1), condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "eq",
            "value": "12-12-2020 12:12:12"
        }
        self.assertDictEqual(self.validator_1.validate_condition(condition_1), condition_1)
        condition_1 = {
            "field": "date_received",
            "operator": "eq",
            "value": "2020-12-12"
        }
        self.assertRaises(ValidationError, self.validator_1.validate_condition, condition_1)

    def test_basic_action_checks(self):
        action_1 = {}
        self.assertRaises(ValidationError, self.validator_1._validate_action, action_1)
        action_1 = {
            "action": "",
        }
        self.assertRaises(ValidationError, self.validator_1._validate_action, action_1)
        action_1 = {
            "action": "invalid",
        }
        self.assertRaises(ValidationError, self.validator_1._validate_action, action_1)
        action_1 = {
            "action": "mark_as_read"
        }
        self.assertDictEqual(self.validator_1._validate_action(action_1), action_1)
        action_1 = {
            "action": "move_to_mailbox",
        }
        self.assertDictEqual(self.validator_1._validate_action(action_1), action_1)
        action_1 = {
            "action": "move_to_mailbox",
        }
        self.assertDictEqual(self.validator_1._validate_action(action_1), action_1)

    def test_action_checks(self):
        action_1 = {
            "action": "move_to_mailbox"
        }
        self.assertRaises(ValidationError, self.validator_1.validate_action, action_1)
        action_1 = {
            "action": "move_to_mailbox",
            "mailbox": ""
        }
        self.assertRaises(ValidationError, self.validator_1.validate_action, action_1)
        action_1 = {
            "action": "move_to_mailbox",
            "mailbox": "test"
        }
        self.assertDictEqual(self.validator_1.validate_action(action_1), action_1)
        action_1 = {
            "action": "mark_as_read"
        }
        self.assertDictEqual(self.validator_1.validate_action(action_1), action_1)
        action_1 = {
            "action": "mark_as_unread"
        }
        self.assertDictEqual(self.validator_1.validate_action(action_1), action_1)
        action_1 = {
            "action": "invalid"
        }
        self.assertRaises(ValidationError, self.validator_1.validate_action, action_1)
