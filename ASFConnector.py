import logging
import requests
import json
from IPCProtocol import IPCProtocolHandler

LOG = None


class ASFConnector:

    def __init__(self, host='127.0.0.1', port='1242', path='/Api', password=None):
        global LOG
        LOG = logging.getLogger('ASFBot.' + __name__)

        self.host = host
        self.port = port
        self.path = path

        LOG.debug(__name__ + " initialized. Host: '%s'. Port: '%s'", host, port)
        self.connection_handler = IPCProtocolHandler(host, port, path, password)

    def get_asf_info(self):
        """" Fetches common info related to ASF as a whole. """
        data = self.connection_handler.get('/ASF')
        LOG.debug(data)
        return data

    def bot_redeem(self, bot, keys):
        """ Redeems cd-keys on given bot. """
        assert type(keys) is list or type(keys) is str
        resource = '/Bot/' + bot + '/Redeem'
        if type(keys) is str:
            keys = [keys]
        data = {'KeysToRedeem': keys}
        response = self.connection_handler.post(resource, payload=data)
        results = response['Result']
        message = ""
        for bot in results:
            message += "Bot {}: \n".format(bot)
            for key in results[bot]:
                if results[bot][key]['Items']:
                    items = ''
                    for item in results[bot][key]['Items']:
                        items += '[{}, {}] '.format(item, results[bot][key]['Items'][item])
                    message += "\t```{}``` {}:{}/{}\n".format(key, items, Result[results[bot][key]['Result']], PurchaseResultDetail[results[bot][key]['PurchaseResultDetail']])
                else:
                    message += "\t```{}``` {}/{}\n".format(key, Result[results[bot][key]['Result']], PurchaseResultDetail[results[bot][key]['PurchaseResultDetail']])
        return message

    def send_command(self, command, arguments='', bot='ASF'):
        LOG.debug("Send command: " + command + ", bot: " + bot + ", arguments: " + arguments)
        asf_command_resource = '/Command'
        user_command_resource = '/' + "+".join(str(command).split())
        user_arguments_resource = '+' + bot + ' ' + "+".join(str(arguments).split())
        resource = asf_command_resource + user_command_resource + user_arguments_resource.strip()
        try:
            response = self.connection_handler.post(resource)
        except requests.exceptions.ConnectionError as connection_error:
            LOG.error("Error sending command %s: %s",
                      command, str(connection_error))
            raise connection_error
        json_response = json.loads(response)
        return json_response["Result"]


PurchaseResultDetail = {
    0: 'NoDetail',
    1: 'AVSFailure',
    2: 'InsufficientFunds',
    3: 'ContactSupport',
    4: 'Timeout',
    5: 'InvalidPackage',
    6: 'InvalidPaymentMethod',
    7: 'InvalidData',
    8: 'OthersInProgress',
    9: 'AlreadyPurchased',
    10: 'WrongPrice',
    11: 'FraudCheckFailed',
    12: 'CancelledByUser',
    13: 'RestrictedCountry',
    14: 'BadActivationCode',
    15: 'DuplicateActivationCode',
    16: 'UseOtherPaymentMethod',
    17: 'UseOtherFunctionSource',
    18: 'InvalidShippingAddress',
    19: 'RegionNotSupported',
    20: 'AcctIsBlocked',
    21: 'AcctNotVerified',
    22: 'InvalidAccount',
    23: 'StoreBillingCountryMismatch',
    24: 'DoesNotOwnRequiredApp',
    25: 'CanceledByNewTransaction',
    26: 'ForceCanceledPending',
    27: 'FailCurrencyTransProvider',
    28: 'FailedCyberCafe',
    29: 'NeedsPreApproval',
    30: 'PreApprovalDenied',
    31: 'WalletCurrencyMismatch',
    32: 'EmailNotValidated',
    33: 'ExpiredCard',
    34: 'TransactionExpired',
    35: 'WouldExceedMaxWallet',
    36: 'MustLoginPS3AppForPurchase',
    37: 'CannotShipToPOBox',
    38: 'InsufficientInventory',
    39: 'CannotGiftShippedGoods',
    40: 'CannotShipInternationally',
    41: 'BillingAgreementCancelled',
    42: 'InvalidCoupon',
    43: 'ExpiredCoupon',
    44: 'AccountLocked',
    45: 'OtherAbortableInProgress',
    46: 'ExceededSteamLimit',
    47: 'OverlappingPackagesInCart',
    48: 'NoWallet',
    49: 'NoCachedPaymentMethod',
    50: 'CannotRedeemCodeFromClient',
    51: 'PurchaseAmountNoSupportedByProvider',
    52: 'OverlappingPackagesInPendingTransaction',
    53: 'RateLimited',
    54: 'OwnsExcludedApp',
    55: 'CreditCardBinMismatchesType',
    56: 'CartValueTooHigh',
    57: 'BillingAgreementAlreadyExists',
    58: 'POSACodeNotActivated',
    59: 'CannotShipToCountry',
    60: 'HungTransactionCancelled',
    61: 'PaypalInternalError',
    62: 'UnknownGlobalCollectError',
    63: 'InvalidTaxAddress',
    64: 'PhysicalProductLimitExceeded',
    65: 'PurchaseCannotBeReplayed',
    66: 'DelayedCompletion',
    67: 'BundleTypeCannotBeGifted'
}

Result = {
    0: 'Invalid',
    1: 'OK',
    2: 'Fail',
    3: 'NoConnection',
    4: 'InvalidPassword',
    5: 'LoggedInElsewhere',
    6: 'InvalidProtocolVer',
    7: 'InvalidParam',
    8: 'FileNotFound',
    9: 'Busy',
    10: 'InvalidState',
    11: 'InvalidName',
    12: 'InvalidEmail',
    13: 'DuplicateName',
    14: 'AccessDenied',
    15: 'Timeout',
    16: 'Banned',
    17: 'AccountNotFound',
    18: 'InvalidSteamID',
    19: 'ServiceUnavailable',
    20: 'NotLoggedOn',
    21: 'Pending',
    22: 'EncryptionFailure',
    23: 'InsufficientPrivilege',
    24: 'LimitExceeded',
    25: 'Revoked',
    26: 'Expired',
    27: 'AlreadyRedeemed',
    28: 'DuplicateRequest',
    29: 'AlreadyOwned',
    30: 'IPNotFound',
    31: 'PersistFailed',
    32: 'LockingFailed',
    33: 'LogonSessionReplaced',
    34: 'ConnectFailed',
    35: 'HandshakeFailed',
    36: 'IOFailure',
    37: 'RemoteDisconnect',
    38: 'ShoppingCartNotFound',
    39: 'Blocked',
    40: 'Ignored',
    41: 'NoMatch',
    42: 'AccountDisabled',
    43: 'ServiceReadOnly',
    44: 'AccountNotFeatured',
    45: 'AdministratorOK',
    46: 'ContentVersion',
    47: 'TryAnotherCM',
    48: 'PasswordRequiredToKickSession',
    49: 'AlreadyLoggedInElsewhere',
    50: 'Suspended',
    51: 'Cancelled',
    52: 'DataCorruption',
    53: 'DiskFull',
    54: 'RemoteCallFailed',
    55: 'PasswordUnset',
    56: 'ExternalAccountUnlinked',
    57: 'PSNTicketInvalid',
    58: 'ExternalAccountAlreadyLinked',
    59: 'RemoteFileConflict',
    60: 'IllegalPassword',
    61: 'SameAsPreviousValue',
    62: 'AccountLogonDenied',
    63: 'CannotUseOldPassword',
    64: 'InvalidLoginAuthCode',
    65: 'AccountLogonDeniedNoMail',
    66: 'HardwareNotCapableOfIPT',
    67: 'IPTInitError',
    68: 'ParentalControlRestricted',
    69: 'FacebookQueryError',
    70: 'ExpiredLoginAuthCode',
    71: 'IPLoginRestrictionFailed',
    72: 'AccountLockedDown',
    73: 'AccountLogonDeniedVerifiedEmailRequired',
    74: 'NoMatchingURL',
    75: 'BadResponse',
    76: 'RequirePasswordReEntry',
    77: 'ValueOutOfRange',
    78: 'UnexpectedError',
    79: 'Disabled',
    80: 'InvalidCEGSubmission',
    81: 'RestrictedDevice',
    82: 'RegionLocked',
    83: 'RateLimitExceeded',
    84: 'AccountLoginDeniedNeedTwoFactor',
    85: 'ItemDeleted',
    86: 'AccountLoginDeniedThrottle',
    87: 'TwoFactorCodeMismatch',
    88: 'TwoFactorActivationCodeMismatch',
    89: 'AccountAssociatedToMultiplePartners',
    90: 'NotModified',
    91: 'NoMobileDevice',
    92: 'TimeNotSynced',
    93: 'SMSCodeFailed',
    94: 'AccountLimitExceeded',
    95: 'AccountActivityLimitExceeded',
    96: 'PhoneActivityLimitExceeded',
    97: 'RefundToWallet',
    98: 'EmailSendFailure',
    99: 'NotSettled',
    100: 'NeedCaptcha',
    101: 'GSLTDenied',
    102: 'GSOwnerDenied',
    103: 'InvalidItemType',
    104: 'IPBanned',
    105: 'GSLTExpired',
    106: 'InsufficientFunds',
    107: 'TooManyPending',
    108: 'NoSiteLicensesFound',
    109: 'WGNetworkSendExceeded',
    110: 'AccountNotFriends',
    111: 'LimitedUserAccount'
}
