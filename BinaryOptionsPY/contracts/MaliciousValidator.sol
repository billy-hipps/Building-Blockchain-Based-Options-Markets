// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

interface ICreateBO {
    function buyContract() external payable;
    function getBuyer() external view returns (address);
    function getPayout() external view returns (uint256);
    function getIsBought() external view returns (bool);
    function timeUpdate(uint256 newTime, uint256 newPrice) external;
    function getBalance() external view returns (uint256);
}

interface IBinaryOption {
    function buy(address payable _buyer) external;
    function getStatus() external view returns (bool, bool, address, uint256);
    function terminate(uint256 _newPrice) external;
}

interface ITimeOracle {
    function update(uint256 newTime, uint256 newPrice) external;
}

contract MaliciousValidator {
    address public owner;
    address public createBO;
    address public binaryOption;
    address public timeOracle;

    event TestResult(string testName, bool passed);

    constructor(address _createBO, address _binaryOption, address _timeOracle) payable {
        owner = msg.sender;
        createBO = _createBO;
        binaryOption = _binaryOption;
        timeOracle = _timeOracle;
    } 

    // T1: Try to withdraw funds from CreateBO or BO without permission
    function testEarlyWithdrawal() external {
        (bool success1, ) = payable(createBO).call(abi.encodeWithSignature("withdraw()"));
        (bool success2, ) = payable(binaryOption).call(abi.encodeWithSignature("withdraw()"));
        emit TestResult("T1: Early withdrawal blocked", !success1 && !success2);
    }

    // T2: Try to overwrite buyer
    function testOverwriteBuyer() external {
        ICreateBO(createBO).buyContract{value: 1 ether}();
        address firstBuyer = ICreateBO(createBO).getBuyer();

        // Try buying again
        (bool success, ) = address(this).call{value: 1 ether}(
            abi.encodeWithSignature("forceBuy()")
        );

        address secondBuyer = ICreateBO(createBO).getBuyer();
        emit TestResult("T2: Buyer overwrite blocked", firstBuyer == secondBuyer);
    }

    // T2 support: fake buy call
    function forceBuy() public payable {
        IBinaryOption(binaryOption).buy(payable(msg.sender));
    }

    // T3: Try to change creator (should not be possible via any public function)
    function testCreatorImmutable() external {
        (bool success, ) = createBO.call(abi.encodeWithSignature("setCreator(address)", address(this)));
        emit TestResult("T3: Creator reassignment blocked", !success);
    }

    // T4: Try to drain funds from contracts
    function testFundDraining() external {
        (bool s1, ) = createBO.call{gas: 100000}(abi.encodeWithSignature("selfdestruct()"));
        (bool s2, ) = binaryOption.call{gas: 100000}(abi.encodeWithSignature("selfdestruct()"));
        emit TestResult("T4: External draining blocked", !s1 && !s2);
    }

    // T5: Try to change time/price manually
    function testOracleEnforcement() external {
        try ICreateBO(createBO).timeUpdate(block.timestamp + 100, 9999) {
            emit TestResult("T5: Only oracle can update time/price  FAILED", false);
        } catch {
            emit TestResult("T5: Only oracle can update time/price  PASSED", true);
        }
    }

    // Cleanup
    function destroy() external {
        require(msg.sender == owner, "Not authorized");
        selfdestruct(payable(owner));
    }

    receive() external payable {}
}
