---
title: "iOS SDK"
excerpt: "This integration guide shows you how to set up and launch an Extole program as quickly as possible with our iOS SDK.\n"
---

## Requirements

[//]: # "What are the minimum requirements for the iOS SDK integration?"

The Extole iOS SDK supports iOS 13.0 and later.

[//]: ___

## Integration

[//]: # "How do I integrate the iOS SDK?"

### Swift Package Manager

1. Open your project in Xcode

2. Go to: File → Add Packages…

3. Enter the repository URL: [https://github.com/extole/ios-sdk](https://github.com/extole/ios-sdk)

4. Choose the latest version

5. Add the package to your target

### Initialize SDK

In your `AppDelegate` class, initialize Extole. You’ll need to provide your Extole program domain.

```swift
class AppDelegate: UIResponder, UIApplicationDelegate, ObservableObject {
    ...
    @Published var extole: Extole = ExtoleImpl(programDomain: "<your-program-domain>")
    ...
}
```

_For a working example, please reference our[Github documentation](https://github.com/extole/ios/blob/master/iOSDemo/iOSDemo/ExtoleCampaign.swift). For more detailed configuration options, see the Advanced Usage section._

### Initialize View

In your `main` method, pass Extole to your view.

```swift
@main
struct ExtoleApp: App {
    ...
    @UIApplicationDelegateAdaptor var delegate: AppDelegate
    ...
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(delegate.extole)
        }
    }
    ....
}
```

_For a working example, please reference our[Github documentation](https://github.com/extole/ios/blob/master/iOSDemo/iOSDemo/iOSDemoApp.swift)._

Initialize the `View` provided by Extole. By default, Extole will use this single view to interact with the customer.

```swift
struct ContentView: View {
    ...
    @EnvironmentObject var extole: Extole
    ...
    var body: some View {
        NavigationView {
              extole.getView()         
        }
    }
    ...
}
```

[//]: ___

## Exchange Data with Extole

[//]: # "How do I send customer information using the iOS SDK?"

### Send Customer Information

Send Extole information about the customer.

```swift
extole.identify("example@test.com", ["partner_user_id": "123"], 
       {(eventId: Id<Event>?, error: Error?) in
            
})
```

You can choose to pass any type of data to describe the customer. Richer data about your customers gives your marketing team the information they need to better segment your program participants and target them with appropriate campaigns.

#### JWT Identification

If you would like to verify the identity of your customers with JWT instead of their email address, use the following method:

```swift
extole.identifyJwt(_ jwt: String, _ data: [String: Any?], _ completion: ((Id<Event>?, Error?) -> Void)?)
```

For more information on generating JWTs, please reference our article on [Verifying Consumers](https://docs.extole.com/docs/verifying-consumers#using-json-web-tokens-jwts).

[//]: ___

### Send Events

[//]: # "How do I send events using the iOS SDK?"

Send Extole events, such as registers, signups, conversions, account openings, and so on.

```swift
extole.sendEvent("my_event")
```

For each event type, you can send additional data. For example, on a conversion event you may want to pass in order ID or order value and so on.

[//]: ___

### Send Call to Action Content

[//]: # "How do I send call-to-action (CTA) content using the iOS SDK?"

Populate a <Glossary>CTA</Glossary> with content from Extole.

CTAs such as mobile menu items can be fully customized in the My Extole Campaign Editor. Each CTA has a designated zone. The following code is an example of how to retrieve a CTA by fetching zone content.

```swift
extole.fetchZone("mobile_cta", [:]) { (zone: Zone?, campaign: Campaign?,   error: Error?) in
    let title = zone?.get("title") as! String? ?? ""
    let image = zone?.get("image") as! String? ?? ""
    // Carry attributes to your view
}


// Send the CTA event when the view is displayed
View {
       .... // Your view    
    }.task {
        zone.viewed()
   }
}

// On CTA tap send the event to Extole
View {
.... // Your view    
}.onTapGesture {
    zone.tap()
}

```

_For a working example, please reference our[Github documentation](https://github.com/extole/ios/blob/master/iOSDemo/iOSDemo/ContentView.swift)._

In order to be able to fetch the `mobile_cta` zone, the zone should be configured in My Extole and should return JSON content containing the `image` and `title`.

> 📘 Important Note
>
> We encourage you to pull CTA content from My Extole because doing so ensures that your menu item or overlay message will reflect the copy and offer you’ve configured for your campaign.

[//]: ___

## Advanced Usage

The following topics cover advanced use cases for the Extole iOS SDK. If you would like to explore any of these options, please reach out to our Support Team at [support@extole.com](mailto:support@extole.com).

### Integrate with a Deep Link Provider

[//]: # "How do I deep link using the iOS SDK?"

Completing a deep link integration is simple once you have integrated with a deep link provider, such as Branch. Send a mobile event to Extole and, based on the configuration of your mobile operations, our framework will execute the corresponding action.

```swift
class AppDelegate: UIResponder, UIApplicationDelegate, ObservableObject {
   @Published var deeplinkProperties: [String: String] = [:]

   func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool 
       Branch.getInstance().initSession(launchOptions: launchOptions) { [self] (params, _) in
           params?.forEach({ (key: AnyHashable, value: Any) in
               deeplinkProperties[key as! String] = String(describing: value)
           })
           extole.sendEvent("deeplink", deeplinkProperties) { _, _ in
           }
       }
       return true
   }
}
```

[//]: ___

### Configure Actions from Events

[//]: # "How do I create actions to fire when events occur using the iOS SDK?"

You can set up a specific action to occur when an event is fired. For example, when a customer taps on your menu item CTA, you may want the event to trigger an action that loads your microsite and shows the share experience.

To set up this type of configuration, you will need to work with Extole Support to set up a zone in My Extole that returns JSON configurations with conditions and actions. The SDK executes actions for conditions that are passing for a specific event.

```json json
{
  "operations": [
    {
      "conditions": [
        {
          "type": "EVENT",
          "event_names": [
            "mobile_cta_tap"
          ]
        }
      ],
      "actions": [
        {
          "type": "VIEW_FULLSCREEN",
          "zone_name": "microsite"
        }
      ]
    }
  ]
}
```

> 📘 Adding additional operations
>
> If you would like to add more operations, you will need to update the zone `mobile_bootstrap`. By default, this zone is not available to be updated. You must have already added the mobile SDK support component. Please reach out to our Support Team at [support@extole.com](mailto:support@extole.com) for help adding this component to your campaign.

#### Supported Actions

The following types of actions are supported by default in our SDK.

| Action Name       | Description                                                                                                                                  |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `PROMPT`          | Display a pop-up notification native to iOS. For example, this could appear when a discount or coupon code has been successfully applied.    |
| `NATIVE_SHARING`  | Open the native share sheet with a predefined message and link that customers can send via SMS or any enabled social apps.                   |
| `VIEW_FULLSCREEN` | Trigger a full screen mobile web view. For example, this could be your microsite as configured in My Extole to display the share experience. |

#### Custom Actions

If you would like to create custom actions beyond our defaults, use the format exhibited in the example below. Please reach out to our Support Team at [support@extole.com](mailto:support@extole.com) if you have any questions.

```swift
import ExtoleMobileSDK

public class CustomAction: Action {
   public static var type: ActionType = ActionType.CUSTOM

   var customActionValue: String?

   public override func execute(event: AppEvent, extole: ExtoleImpl) {
       extole.getLogger().setLogLevel(level: LogLevel.disable)
   }

   init(customActionValue: String) {
       super.init()
       self.customActionValue = customActionValue
   }

   override init() {
       super.init()
   }

   public override func getType() -> ActionType {
       ActionType.CUSTOM
   }

   public required init?(map: Map) {
       super.init()
   }

   public override func mapping(map: Map) {
       customActionValue <- map["custom_action_value"]
   }

   public var description: String {
       return "CustomAction[customActionValue:\(customActionValue)]"
   }
}
```

#### Register Custom Actions

```swift sw
Action.customActionTypes["CUSTOM_ACTION"] = CustomAction()
```

[//]: ___
