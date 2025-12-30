Feature: iOS Screen Recording
  As a QA Automation Engineer
  I want to record the screen of an iOS device during tests
  So that I can analyze the execution later

  Scenario: Record a short session on iOS device
    Given the iOS device is connected and ready
    When I start the screen recording
    And I wait for "5" seconds
    Then I stop the recording and save it to "output/bdd_recordings"
    And the recorded video file should exist
