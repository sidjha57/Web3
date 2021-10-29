// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

//import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

interface AggregatorV3Interface {
  function decimals() external view returns (uint8);

  function description() external view returns (string memory);

  function version() external view returns (uint256);

  // getRoundData and latestRoundData should both raise "No data present"
  // if they do not have data to report, instead of returning unset values
  // which could be misinterpreted as actual reported values.
  function getRoundData(uint80 _roundId)
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

  function latestRoundData()
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );
}


/* Interfaces compile down to an ABI
    ABI = Application Binary Interface
    The ABI tells solidity and other programming languages how it can interact with another contract
    Anytime you want to interact with an already deployed smart contarct you will need an ABI
    Interfaces compile down to an ABI
    Always need an ABI to interact with a contract
*/
contract FundMe {
    using SafeMathChainlink for uint256;
    /*
    The directive using A for B; can be used to attach library
    functions (from the library A) to any type(b) in the context of a contract.
    */
    
    mapping (address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    
    constructor() public {
        owner = msg.sender;
    }
    
    
    function fund() public payable {
        // // $1
        // uint256 minimumUSD =   10 ** 18;
        // require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!"); // Revert
        
        
        addressToAmountFunded[msg.sender] += msg.value;
        // minimum transaction amount required
        //  what the ETH -> USD conversion rate 
        funders.puch(msg.sender);
    }
    
    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        return priceFeed.version();
    } 
    function getPrice() public view returns(uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256 (answer * 1000000000);
    }
    
    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
        //  0.0000041476559003
        
    }
    
    /*Modifiers are used to change the behavior of a function in a declarative way  */
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function withdraw() payable onlyOwner public {
        // only want the contract admin/owner
        // require msg.sender = owner
        //require(msg.sender == owner); after adding modifier this is not required
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
    
}