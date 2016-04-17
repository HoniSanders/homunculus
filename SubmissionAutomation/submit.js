/******************************************************
* Signs into MLB .com, and submits picks for given dates based on submission file.
* Each line in the submission file should be of the form "Three letter month day,player name"
* See SampleSelection.txt for an example
*******************************************************/

var casper = require('casper').create({
    // verbose: true,
    // logLevel: "debug"
});

var x = require('casper').selectXPath;

var fs = require('fs');
var utils = require('utils');
var selectionText = fs.read('SampleSelection.txt');
var selectionComponents = selectionText.split(",");
var dateComponents = selectionComponents[0].split(" ");
var player = selectionComponents[1].trim();

casper.start('https://secure.mlb.com/enterworkflow.do?flowId=fantasy.bts.btsloginregister&template=mobile&forwardUrl=http://mlb.mlb.com/mlb/fantasy/bts/y2016/');

casper.waitForSelector("#login-form", function() {
    this.echo("found login");
    this.fill('form[action="/authenticate.do"]', { 'emailAddress': 'siweiss@gmail.com', 'password': 'lucy2306' }, true);
});

// login is slow, so wait for full page load
casper.wait(5000);

var dateSelector = '//span[text()="' + dateComponents[0].trim() + '"]/following-sibling::span[text()="' + dateComponents[1].trim() + '"]';
var makePickSelector = dateSelector + '/../../../..//td[@class="bts__make-pick"]';

// Find the correct date
casper.waitForSelector(x(dateSelector), function() {
    this.echo("found table");
    this.click(x(dateSelector + '/../../../..//ul[@class="player-info-rows"]'));
});

// Select the custom player form
casper.waitForSelector(x(makePickSelector + '//a[text()="Custom"]'), function() {
    this.echo("found custom");
    this.click(x(makePickSelector + '//a[text()="Custom"]'));
});

// Apply to open the player's list
casper.waitForSelector(x('//button[text()="Apply"]'), function () {
    this.echo("found apply");
    this.click(x('//button[text()="Apply"]'));
});

var playerSelector = '//div[contains(text(), "' + player + '")]';
// Select the player
casper.waitForSelector(x(playerSelector), function () {
    this.echo("found player");
    this.click(x(playerSelector + '/../../..//button'));
});

// Wait for the pick to finish
casper.wait(5000);

casper.run();